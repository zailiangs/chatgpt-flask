import functools

import pymysql
from flask import Flask
from flask_cors import CORS

from chat.api.chat import chat_bp
from config import Config

app = Flask(__name__)
# 加载配置类
app.config.from_object(Config)
# 初始化CORS扩展
CORS(app, supports_credentials=True, resources={r"/*": {"origins": "*"}})
# 注册蓝图(用的文件名)
app.register_blueprint(chat_bp)
# 配置数据库连接
connect = pymysql.connect(host="localhost", port=3306, user="root", password="xxxx",
                          db="db", charset="utf8", autocommit=True, connect_timeout=10, read_timeout=10)


# 检测数据库连接是否可用, 如果不可用则重连
def check_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            connect.ping(reconnect=True)
        except Exception as e:
            app.logger.error("[Sun] The database connection is abnormal. Reconnecting..., Error: %s", e)
            connect.close()
            connect.connect()
        return func(*args, **kwargs)

    return wrapper


@check_connection
def execute_sql(sql, args=None):
    try:
        cursor = connect.cursor()
        cursor.execute(sql, args)
        connect.commit()
    except Exception as e:
        app.logger.error("[Sun] Database operation exception, Error: %s", e)
        connect.rollback()
        return False
    return True


@check_connection
def fetchall_sql(sql, args=None):
    try:
        cursor = connect.cursor()
        cursor.execute(sql, args)
        results = cursor.fetchall()
        return results
    except Exception as e:
        app.logger.error("[Sun] Database operation exception, Error: %s", e)
        connect.rollback()
        return None


@check_connection
def fetchone_sql(sql, args=None):
    try:
        cursor = connect.cursor()
        cursor.execute(sql, args)
        result = cursor.fetchone()
        return result
    except Exception as e:
        app.logger.error("[Sun] Database operation exception, Error: %s", e)
        connect.rollback()
        return None


@app.route('/')
def hello_world():
    return 'Welcome to the AI world!'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
