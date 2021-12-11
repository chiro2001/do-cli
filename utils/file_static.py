import re
import os
from flask import Flask, send_file
from utils.logger import logger
from data.config import config


# 检查请求路径有效性
def is_file_path_legal(static_path: str, path: str) -> bool:
    # 文件要存在
    file_path = get_static_file_path(static_path, path)
    # logger.info('abspath: %s' % os.path.abspath(file_path))
    # logger.info('os.path.exists(file_path): %s' % os.path.exists(file_path))
    # logger.info('os.path.isfile(file_path): %s' % os.path.isfile(file_path))
    if not (os.path.exists(file_path) and os.path.isfile(file_path)):
        return False
    # 不能使用两个点向上目录
    if '..' in re.split(r"[/\\]", file_path):
        return False
    return True


def get_static_file_path(static_path: str, path: str):
    return os.path.join(static_path, path)


app = Flask(__name__, static_folder=config.data['file_server']['static_path'])


# 统一错误处理信息
@app.errorhandler(404)
def handler_404(error):
    logger.error(f"{error}")
    return f"<p>{error}</p><br><p>你来到了知识的荒原——</p>"


@app.route("/<path:path>")
def file_server(path: str):
    if path in config.data['file_server']['routers']:
        return index()
    file_path = get_static_file_path(config.data['file_server']['static_path'], path)
    if not is_file_path_legal(config.data['file_server']['static_path'], path):
        logger.warning(f'visiting illegal path: {file_path}')
        logger.warning(f'visiting illegal absolutely path: {os.path.abspath(file_path)}')
        return handler_404("路径不合法"), 404
    # 这里有些问题...得上一层文件夹
    return send_file(os.path.join('../', get_static_file_path(config.data['file_server']['static_path'], path)))


@app.route("/")
def index():
    return file_server(config.data['file_server']['index'])


if __name__ == '__main__':
    app.run("0.0.0.0", port=8080)
