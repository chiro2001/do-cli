import argparse
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.serving import run_simple
from data.config import Constants
import logging
from utils.logger import logger

# from utils.file_static import app as app_file
from apis.api_main import app as app_api

# 只显示错误消息
logger_werkzeug = logging.getLogger('werkzeug')
logger_werkzeug.setLevel(logging.ERROR)
# logger_werkzeug.setLevel(logging.DEBUG)

# 中间件
# dm = DispatcherMiddleware(app_file, {Constants.API_PATH: app_api})

app = app_api
dm = app


def main():
    host, port = Constants.RUN_LISTENING, Constants.RUN_PORT
    parser = argparse.ArgumentParser(
        description='Manage your Digital Ocean droplets by simple RESTful-API.')
    parser.add_argument('-l', '--listen', required=False, default=host,
                        help=f'specific host to listen on. (default {host})')
    parser.add_argument('-p', '--port', required=False, default=port,
                        help=f'specific port to listen on. (default {port})')
    args = parser.parse_args().__dict__
    host, port = args.get('listen'), int(args.get('port'))
    logger.info(f'Digital Ocean API server started at {host}:{port}')
    run_simple(host, port, dm, use_reloader=Constants.RUN_USE_RELOAD)


if __name__ == '__main__':
    main()
