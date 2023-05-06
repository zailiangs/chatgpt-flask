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
connect = pymysql.connect(host="sh-cdb-mns9cip2.sql.tencentcdb.com", port=63682, user="root", password="Passgz6374",
                          db="yk_rank", charset="utf8", autocommit=True)


def execute_sql(sql, args=None):
    try:
        cursor = connect.cursor()
        cursor.execute(sql, args)
        connect.commit()
    except Exception as e:
        print(e)
        connect.rollback()
        return False
    return True


def fetchall_sql(sql, args=None):
    try:
        cursor = connect.cursor()
        cursor.execute(sql, args)
        results = cursor.fetchall()
        return results
    except Exception as e:
        print(e)
        connect.rollback()
        return None


def fetchone_sql(sql, args=None):
    try:
        cursor = connect.cursor()
        cursor.execute(sql, args)
        result = cursor.fetchone()
        return result
    except Exception as e:
        print(e)
        connect.rollback()
        return None


@app.route('/')
def hello_world():
    return 'Welcome to the AI world!'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
