import os

MAX_CLIENT_NAME_LENGTH = 100
MAX_OPERATION_DESCRIPTION_LENGTH = 255
DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'

LOGFILE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs', 'main.log')

LOGGING = {
    'version': 1,
    'formatters': {
        'file': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        },
    },
    'handlers': {
        'file': {
            'class': 'logging.FileHandler',
            'formatter': 'file',
            'filename': LOGFILE_PATH,
            'level': 'DEBUG'
        },
    },
    'loggers': {
        '': {
            'handlers': ['file'],
            'level': 'DEBUG'
        }
    }
}
