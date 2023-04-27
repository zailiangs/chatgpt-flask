import json

import openai
from flask import request, Response, Blueprint
from flask_cors import cross_origin

import app
from config import Logger

# 一个蓝图对象
chat_bp = Blueprint('chat', __name__, url_prefix='/api')
# 初始化日志
logger = Logger('./logs/chat.log')


# AI聊天
@cross_origin()
@chat_bp.route('/chat', methods=['GET'])
def chat():
    content = request.args.get('content')
    openai.api_key = "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"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": content}
        ],
        stream=True,
    )

    def generate():
        for chunk in response:
            chunk_message = chunk['choices'][0]['delta']
            loads = json.loads(json.dumps(chunk_message))
            # 将单引号替换为双引号
            chunk_data = str(loads).replace("'", "\"")
            # 返回event-stream类型的响应
            yield 'data: {}\n\n'.format(chunk_data)

    return Response(generate(), mimetype='text/event-stream')


# 保存用户聊天数据
@chat_bp.route('/saveRecord', methods=['POST'])
def save_record():
    content = request.form.get('content')
    work_id = request.form.get('work_id')
    cur = app.get_db_cursor()
    cur.execute("insert into ai_user_question (work_id, question) values (%s, %s)", (work_id, content))
    commit = cur.connection.commit()
    # 如果失败的话，就回滚
    if commit == 0:
        cur.connection.rollback()
    app.close_db_cursor(error=None)
    return "success"


# 服务端推送协议测试
@chat_bp.route('/sse', methods=['GET'])
def sse():
    content = request.args.get("content")
    logger.info("--------------------SSE API Call")

    def event_stream():
        data_list = [{"role": "assistant"}, {"content": "你好"}, {"content": "!"}, {"content": "有"},
                     {"content": "什么"}, {"content": "可以"}, {"content": "帮助"}, {"content": "您"},
                     {"content": "的"}, {"content": "吗?"}, {"content": " 内容测试词: "}, {"content": content}, {}]
        for data in data_list:
            data_replace = str(data).replace("'", '"')
            yield 'data: {}\n\n'.format(data_replace)

    return Response(event_stream(), mimetype='text/event-stream')


# 测试数据库连接
@chat_bp.route('/test', methods=['GET'])
def test():
    cur = app.get_db_cursor()
    cur.execute("select * from ai_user_question")
    result = cur.fetchall()
    app.close_db_cursor(error=None)
    return str(result)


@chat_bp.route('/testAdd', methods=['GET'])
def test_add():
    cur = app.get_db_cursor()
    cur.execute("insert into ai_user_question (work_id, question) values (%s, %s)", (1, "testtesttest"))
    commit = cur.connection.commit()
    # 如果失败的话，就回滚
    if commit == 0:
        cur.connection.rollback()
    app.close_db_cursor(error=None)
    return "success"
