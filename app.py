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
