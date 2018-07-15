import os
import logging.config

HOST = 'localhost'
PORT = 8080

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_FILES_DIR = os.path.join(PROJECT_DIR, 'static')
SOCKET_BACKLOG_SIZE = 5
FILE_CHUNK_SIZE = 1024 * 1024
RECV_BUFSIZ = 1024
THREAD_POOL_SIZE = 10

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(asctime)s %(module)s %(process)d %(thread)d %(levelname)s %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'file-dog': {
            'level': 'DEBUG',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'formatter': 'verbose',
            'filename': 'run.log',
            'when': 'midnight'
        }
    },
    'loggers': {
        'httpy': {
            'handlers': ['file-dog', 'console'],
            'propagate': False,
            'level': 'INFO'
        }
    }
}


def setup_logging():
    logging.config.dictConfig(LOGGING)