import logging
import os
from logging.handlers import RotatingFileHandler

from flask import Flask
from flask_cors import CORS

from controller.ChatGPTController import ChatGPT

app = Flask(__name__)
# 初始化CORS扩展
CORS(app, resources={r"/*": {"origins": "*"}})
# 注册蓝图(用的文件名)
app.register_blueprint(ChatGPT)


@app.route('/')
def hello_world():
    app.logger.info('Processing default request...')
    return 'Hello World!'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

# 定义日志处理器，设置日志级别为 INFO，并将日志写入到文件中
if not os.path.exists('logs'):
    os.mkdir('logs')
handler = RotatingFileHandler('logs/app.log', maxBytes=10240, backupCount=10)
handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
handler.setLevel(logging.INFO)

# 将日志处理器添加到默认的日志记录器中
app.logger.addHandler(handler)
