import json

import openai
from flask import request, Response, Blueprint
from flask_cors import cross_origin

import app
from config import Logger

# 一个蓝图对象
chat_bp = Blueprint('chat', __name__)
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
    work_id = request.args.get('work_id')
    # 数据插入
    cur = app.get_db_cursor()
    cur.execute("insert into ai_user_question (work_id, question) values (%s, %s)", (work_id, content))
    cur.connection.commit()
    app.close_db_cursor(error=None)

    def generate():
        for chunk in response:
            chunk_message = chunk['choices'][0]['delta']
            loads = json.loads(json.dumps(chunk_message))
            # 将单引号替换为双引号
            chunk_data = str(loads).replace("'", "\"")
            # 返回event-stream类型的响应
            yield 'data: {}\n\n'.format(chunk_data)

    return Response(generate(), mimetype='text/event-stream')


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
