import re
import time
from datetime import datetime
from functools import partial
from traceback import format_exc 
import json

# Import appropriate modules from the client library.
import pytz
from googleads import dfp
from suds import MethodNotFound, WebFault
from suds.sax.text import Text
import transpose

from dfp_sync import utils


class DFPService:
  """
  An abstract wrapper for connecting to a DFP Service via API.
  """

  VERSION = 'v201511'

  # the list of services that downloadable from DFP.
  SERVICES = [
    'AdUnit',
    # 'AdUnitSize',
    'ActivityGroup', 
    'Activity',
    'AdExclusionRule',
    'AdRule', 
    'AudienceSegment', 
    'BaseRate',
    'Company', 
    'Contact', 
    'ContentBundle',
    'ContentMetadataKeyHierarchy',
    'Content',
    'Creative',
    'CreativeSet',
    'CreativeTemplate',
    'CreativeWrapper',
    'CustomField',
    # 'CustomTargeting',
    # 'ExchangeRate',
    # 'Forecast',
    # 'Inventory',
    'Label',
    'LineItemCreativeAssociation',
    'LineItem',
    'LineItemTemplate',
    # 'LiveStreamEvent',
    'Network',
    'Order',
    # 'Package',
    'Placement',
    'PremiumRate',
    'Product',
    # 'ProductPackage',
    # 'ProductPackageItem',
    # 'ProductTemplate',
    'ProposalLineItem',
    'Proposal',
    # 'PublisherQueryLanguage',
    'RateCard',
    # 'ReconciliationOrderReport',
    # 'ReconciliationReportRow',
    # 'ReconciliationLineItemReport',
    # 'ReconciliationReport',
    # 'Report',
    'SharedAdUnit',
    'SuggestedAdUnit',
    'Team',
    'User',
    'UserTeamAssociation'
    # 'WorkflowRequest'
  ]

  def __init__(self, name, config, **kw):
    self.client = dfp.DfpClient.LoadFromStorage(config)
    self.version = kw.get('version', self.VERSION)
    self.table_name = utils.no_camel(name)
    self._set_method_and_service(name)
    self.service = self.client.GetService(
      self.name, version=self.version)
    self.schema = transpose.new(title=self.table_name)

  def _set_method_and_service(self, name):
    """
    bespoke hacks for auto-generating correct 
    service name and query method
    """ 

    self.name = "{}Service".format(name)
    self.q_method = 'get{}sByStatement'.format(name)
    self.accepts_statment = True
    if 'ys' in self.q_method:
      self.q_method = self.q_method.replace('ys', 'ies')
    if 'Contents' in self.q_method:
      self.q_method = self.q_method.replace('Contents', 'Content')
    if 'Network' in self.name:
      self.q_method = 'getAllNetworks'
      self.accepts_statment = False
    if name.startswith('AdUnit'):
      self.name = "InventoryService"


  def get_records(self, **kw):
    """
    Query statement with a filter, parsing response into a stream of simple, flat python dictionaries,
    and optionally paginating through resultset
    """
    print 'get records'
    # Create statement object to select all items
    if not kw.get('where'):
      statement = dfp.FilterStatement()
    else:
      statement = dfp.FilterStatement(kw.get('where'))

    # Get method for fetching items by ststement
    try:
      method = getattr(self.service, self.q_method)
    
    except MethodNotFound as e:
      print(e.message)
      return
    
    except WebFault as e:
      print(e.message)
      return 
    
    return self._exec_statement(method, statement, **kw)


  def _exec_statement(self, method, statement, **kw):
      """
      fetch a dfp statement, optionally paginating through resultset
      """
      kw.setdefault('max_retries', 3)
      kw.setdefault('backoff', 4.2) # factor by which to increment sleep between retries.
      kw.setdefault('page', True)
      
      def _exec(statement):    
        
        if not self.accepts_statment:
          response = method()
        else:
          response = method(statement.ToStatement())
        return self._parse_response(response, **kw)
      
      # fetch first result set
      if not kw['page']:
        for result in _exec(statement):
          yield result

      # paginate + retry
      else:    
        
        while True:
          tries = 0

          # fetch results with retries
          while True:
            tries += 1
            
            try:
              results = _exec(statement)
              break
            
            except Exception as e:
              if tries > kw['max_retries']:
                print("ERROR: {0}".format(format_exc()))
                raise 
              print("WARNING on try {0}  of {backoff}: {1}".format(tries, format_exc(), **kw))
              
              time.sleep(tries * kw['backoff'])
          
          # check for end of results
          if not len(results):
            break
          
          # yield results
          for result in results:
            yield result
          
          # generate next statement
          statement.offset += kw.get('offset', dfp.SUGGESTED_PAGE_LIMIT)

  def _parse_response(self, response, **kw):
    """
    Parse a response into individual records.
    """
    if 'results' not in response and isinstance(response, list):
      results = response
    else:
      results = getattr(response, 'results', [])
    func = partial(self._parse_record, **kw)
    return map(self._parse_record, results)

  def _parse_record(self, record, parent_key='', sep='_', flatten=False):
    """
    Recursively parse a Suds record into a simple dictionary.
    """
    nu = {}

    for key in dir(record):
      # ignore internal methods
      if key.startswith('_'): 
        continue 
      
      # standardize and flatten key
      key = "{0}{1}{2}".format(parent_key, sep, key) if parent_key else key
      key = utils.no_camel(key)
        
      # get an attribute.
      attr = getattr(record, key, None)

      # passthrough simple/null fields    
      if not attr or isinstance(attr, (int, float, bool, long, str, unicode)):
        nu[key] = attr

      # check for suds Text object
      elif isinstance(attr, Text):
        nu[key] = unicode(attr)

      # parse datetime fields  -- this is ugly.
      elif 'DateTime' in attr.__class__.__name__:
        nu[key] = self._parse_date_time(attr)

      # parse lists
      elif isinstance(attr, list):
        nu[key] = []
        for r in attr:
          r = self._parse_record(r)
          if len(r.keys()):
            nu[key].append(r)

      # recurse on suds models -- this is ugly.
      elif attr.__module__ and 'sudsobject' in attr.__module__:
        if flatten:
          nu.update(self._parse_record(attr, key))
        else:
          nu[key] = self._parse_record(attr)

      # everything else is non-suds crud:

      # final check for errant nulls:
      if key in nu and nu[key] == 'NONE': 
        nu[key] = None
    # update schema
    self.schema.update(nu)
    return nu

  def _parse_date_time(self, obj):
    """
    Parse a suds.sudsobject.DateTime object into an isoformat string.
    """
    return datetime(
        year = obj.date.year,
        month = obj.date.month,
        day = obj.date.day,
        hour = obj.hour,
        minute = obj.minute,
        second = obj.second,
        tzinfo=pytz.timezone(obj.timeZoneID)
      ).isoformat()

