from flask import Flask
from controller.ChatGPTController import ChatGPT

app = Flask(__name__)

# 注册蓝图(用的文件名)
app.register_blueprint(ChatGPT)


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
