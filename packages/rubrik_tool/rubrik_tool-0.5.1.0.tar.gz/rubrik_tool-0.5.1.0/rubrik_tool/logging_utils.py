import os
import sys
import logging

if sys.version_info < (2, 7):
    from dictconfig import dictConfig
else:
    from logging.config import dictConfig

ISO_1806_TIMESTAMP_FORMAT = '%Y-%m-%dT%H:%M:%S%z'
LOG_FORMAT = '%(asctime)s %(levelname)s ' + \
    '<%(process)d.%(threadName)s> [%(name)s] %(message)s'

MODULES_TO_QUIET = [
    'cassandra.cluster',
    'cassandra.connection',
    'cassandra.io.asyncorereactor',
    'cassandra.pool',
    'celery.bootsteps',
    'celery.pool',
    # Re-enabling 'celery.worker.strategy' for improved diagnosis.
    # TODO(kt) Quiet this one again once we've resolved whatever is going on
    # with duplicate task IDs seen in
    # https://app.asana.com/0/16400954177758/22077150833478
    # 'celery.worker.strategy',
    'kombu.common',
    'paramiko.transport',
    'requests.packages.urllib3.connectionpool',
    'urllib3.connectionpool',
    'urllib3.util.retry'
]


def config(log_timestamp_format=ISO_1806_TIMESTAMP_FORMAT,
           log_file_name=None,
           log_file_level=None,
           console_handler_level=None,
           console_handler_stream=None):
    file_handler = {
        'class': 'logging.NullHandler',
        'formatter': 'standard',
        'level': 'DEBUG' if log_file_level is None else log_file_level
    }
    if log_file_name is not None:
        if console_handler_level is None:
            console_handler_level = 'INFO'
        file_handler['class'] = 'logging.FileHandler'
        file_handler['filename'] = log_file_name

    # Set the default console handler level after higher priority settings
    # have had their chance to set it.
    if console_handler_level is None:
        console_handler_level = 'INFO'

    dictConfig({
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'standard': {
                'format': LOG_FORMAT,
                'datefmt': log_timestamp_format
            }
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': 'standard',
                'level': console_handler_level,
                'stream': console_handler_stream
                if console_handler_stream is not None else 'ext://sys.stdout'
            },
            'file': file_handler
        },
        'loggers': {
            '': {
                'handlers': [
                    'console',
                    'file'
                ],
                'level': 'DEBUG',
                'propagate': True
            }
        }
    })

    quiet_modules()

# Quiet down verbose modules that would create log noise.
def quiet_modules():
    for name in MODULES_TO_QUIET:
        logging.getLogger(name).setLevel(logging.ERROR)


def init_logging(console_handler_stream=None,
                 log_to_file=True,
                 log_file_level=None):
    prog_name = os.path.basename(sys.argv[0])
    if log_to_file:
        log_file_name = os.environ.get('LOG_FILE', prog_name + '.log.txt')
    else:
        log_file_name = None
    console_handler_level = None
    if 'LOG_LEVEL' in os.environ:
        console_handler_level = os.environ.get('LOG_LEVEL').upper()
    if 'LOG_FILE_LEVEL' in os.environ:
        log_file_level = os.environ.get('LOG_FILE_LEVEL').upper()
    config(log_file_name=log_file_name,
           log_file_level=log_file_level,
           console_handler_level=console_handler_level,
           console_handler_stream=console_handler_stream)
