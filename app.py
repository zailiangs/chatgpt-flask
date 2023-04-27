from flask import Flask, g
from flask_cors import CORS
from pymysql import connect

from chat.api.chat import chat_bp

app = Flask(__name__)
# 初始化CORS扩展
CORS(app, supports_credentials=True, resources={r"/*": {"origins": "*"}})
# 注册蓝图(用的文件名)
app.register_blueprint(chat_bp)
# 配置数据库连接
connect = connect(host="1.117.243.197", port=53306, user="root", password="Passgz6374", db="yk_rank", charset="utf8")


def get_db_cursor():
    if 'db' not in g:
        g.db = connect.cursor()
    return g.db


@app.teardown_appcontext
def close_db_cursor(error):
    if hasattr(g, 'db'):
        g.db.close()


@app.route('/')
def hello_world():
    return 'Welcome to the AI world!'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
