import logging

from server.server import run_server
from config import HOST, PORT, setup_logging


log = logging.getLogger('httpy.run')


if __name__ == '__main__':
    setup_logging()

    try:
        run_server(host=HOST, port=PORT)
    except KeyboardInterrupt:
        log.info('http stopped')
