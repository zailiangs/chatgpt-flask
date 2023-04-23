from flask import Flask
from flask_cors import CORS

from chat.api.chat import gpt

app = Flask(__name__)
# 初始化CORS扩展
CORS(app, supports_credentials=True, resources={r"/*": {"origins": "*"}})
# 注册蓝图(用的文件名)
app.register_blueprint(gpt)


@app.route('/')
def hello_world():
    return 'Welcome to the AI world!'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
