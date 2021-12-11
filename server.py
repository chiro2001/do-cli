from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.serving import run_simple
from data.config import Constants
import logging
from utils.logger import logger

from utils.file_static import app as app_file
from apis.api_main import app as app_api

# 只显示错误消息
logger_werkzeug = logging.getLogger('werkzeug')
logger_werkzeug.setLevel(logging.ERROR)
# logger_werkzeug.setLevel(logging.DEBUG)

host, port = Constants.RUN_LISTENING, Constants.RUN_PORT

# 中间件
dm = DispatcherMiddleware(app_file, {Constants.API_PATH: app_api})

if __name__ == '__main__':
    logger.info(f'server started at {host}:{port}')
    run_simple(host, port, dm, use_reloader=Constants.RUN_USE_RELOAD)
