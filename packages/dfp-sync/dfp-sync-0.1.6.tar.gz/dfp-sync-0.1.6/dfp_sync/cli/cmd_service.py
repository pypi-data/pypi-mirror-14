"""
Sync DFP API Services => Amazon S3 As AVRO
"""
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

from traceback import format_exc 

from dfp_sync.common import DFPService
from dfp_sync.utils import threaded
from dfp_sync.utils import write_avro_to_s3
from dfp_sync.utils import write_to_s3


def setup(parser):
  """
  Arguments for the service command.
  """
  srv_parser = parser.add_parser("service", 
    help="Sync Doubleclick API Service Data.")

  srv_parser.add_argument('service_name', type=str, default=None,
    help='The service name to sync.', choices=DFPService.SERVICES + ["All"])

  srv_parser.add_argument('-c', '--config', type=str, default='googleads.yaml',
    help='The path to your googleads.yaml file.')

  srv_parser.add_argument('-n', '--chunk-size', type=int, 
    help='The number of records to dump per file', default=15000)

  srv_parser.add_argument('-f', '--format', default='avro', choices=['avro', 'json.gz'],
    help='The format to export files in.')

  srv_parser.add_argument('-w', '--where', type=str, default=None,
    help='Optional PQL filter statement to apply to a service. Ignored when service_name == "All"')

  srv_parser.add_argument('-l', '--log-every', type=int, default=1000,
    help='How often to log process (in number of records).')

  srv_parser.add_argument('-j', '--n-jobs', type=int, default=5,
    help='The number of services to concurrently access.')

  srv_parser.add_argument('-d', '--s3-data-dir', type=str, 
    help='The S3 Bucket where the files should be stored.')

  srv_parser.add_argument('-s' , '--s3-schema-path', type=str, 
    help='The S3 Bucket where the files should be stored.')

  return 'service', run


def run(opts):
  print opts
  if opts.service_name == 'All':
    threaded(export_service, 
             DFPService.SERVICES, 
             n_jobs=opts.n_jobs, 
             opts=opts)
  else:
    return export_service(opts.service_name, opts=opts)


def export_service(name, **kw):
  """
  Transfer All Records from a DFP service 
  to avrofiles on S3.
  """
  if not name:
    name = opts.service_name
  opts = kw.get('opts')
  print('INFO: Exporting {0}'.format(name))
  
  # connect to client + service + schmema
  service = DFPService(name, config=opts.config)

  # export all records from service and 
  # write chunks of avro to s3.
  n_records = 0
  part = 1
  records = []

  for record in service.get_records(where=opts.where):

    # increment record counter
    n_records += 1
    records.append(record)

    # write chunks of records to s3.
    if n_records % opts.chunk_size == 0:

      fp = '%s/%03d.avro' % (opts.s3_data_dir, part)
      print("INFO: Dumping part {0} of {1} to {2}".format(part, name, fp))
      write_avro_to_s3(fp, 
                       records, 
                       service.schema.to('avro'),
                       key=opts.aws_key,
                       secret=opts.aws_secret)
      records = []
      part += 1
    
    # log record count for service.
    if n_records % opts.log_every == 0:
      print('INFO: Processed {0} records for {1}'.format(n_records, name))

  # write remaining records to s3.
  if len(records):
    
    print("INFO: Finishing up processing of {0} records from {1}"\
      .format(n_records, name))
    
    fp = '%s/%06d.avro' % (opts.s3_data_dir, part)
    print("INFO: Dumping part {0} of {1} to {2}".format(part, name, fp))
    write_avro_to_s3(fp, 
                     records, 
                     service.schema.to('avro'),
                     key=opts.aws_key,
                     secret=opts.aws_secret)

  # write schema for created tables.
  if n_records > 0:

    print("INFO: Writing {0} schema to {1}".format(opts.s3_schema_path, fp))
    write_to_s3(fp, 
                service.schema.to('avsc'),
                key=opts.aws_key,
                secret=opts.aws_secret)


