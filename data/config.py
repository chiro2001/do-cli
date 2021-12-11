import os
from utils.logger import logger
import secrets
import platform


class Constants:
    # Version info
    VERSION = "0.2.0"
    ADMIN = "chiro"
    EMAIL = "Chiro2001@163.com"
    # Environment
    ENVIRONMENT = os.environ.get("ENV") if os.environ.get("ENV") is not None else (
        "release" if platform.system() == 'Linux' else "dev")
    # Find
    FIND_LIMIT = 30
    # FIND_LIMIT = 8
    # API config
    API_PATH = '/api/v2'
    # Running config
    RUN_LISTENING = "0.0.0.0"
    RUN_PORT = int(os.environ.get("PORT", 9981))
    RUN_USE_RELOAD = False
    RUN_FRONTEND_PROXY = False
    # Request API
    REQUEST_UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:86.0) Gecko/20100101 Firefox/86.0"


class Statics:
    pass


class Config:
    def __init__(self):
        self.data_default = {
            "version": Constants.VERSION,
            "api_server": {
                "upgradable": True,
                "api_prefix": Constants.API_PATH
            },
            "file_server": {
                "upgradable": True,
                "static_path": "./public",
                "index": "index.html",
                "routers": []
            }
        }
        self.data = self.data_default


config = Config()
