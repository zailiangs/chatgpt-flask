import json
import uuid

import openai
from flask import request, Response, Blueprint
from flask_cors import cross_origin

import app
from config import Logger, Result

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
            chunk_data = str(loads).replace("'", "\"")
            # 返回event-stream类型的响应
            yield 'data: {}\n\n'.format(chunk_data)

    return Response(generate(), mimetype='text/event-stream')


# 新建会话
@chat_bp.route('/newSession', methods=['POST'])
def new_session():
    uid = request.json.get("uid")
    session_id = str(uuid.uuid4())
    session_name = "New Chat"
    status = app.execute_sql("insert into ai_session (uid, session_id, session_name) values (%s, %s, %s)",
                             (uid, session_id, session_name))
    return Result.success(msg="新建成功") if status else Result.error(msg="新建失败")


# 获取会话列表
@chat_bp.route('/getSessionList', methods=['GET'])
def get_session_list():
    uid = request.args.get("uid")
    results = app.fetchall_sql("select session_id, session_name from ai_session where is_delete = 0 and uid = %s "
                               "order by create_time desc", (uid,))
    data = []
    if results is not None:
        for result in results:
            row_data = {'session_id': result[0], 'session_name': result[1]}
            data.append(row_data)
    return Result.success(data=data)


# 重命名会话名称
@chat_bp.route('/renameSession', methods=['POST'])
def rename_session():
    session_id = request.json.get("session_id")
    session_name = request.json.get("session_name")
    status = app.execute_sql("update ai_session set session_name = %s where session_id = %s",
                             (session_name, session_id))
    return Result.success(msg="修改成功") if status else Result.error(msg="修改失败")


# 删除会话
@chat_bp.route('/deleteSession', methods=['POST'])
def delete_session():
    session_id = request.json.get("session_id")
    status = app.execute_sql("update ai_session set is_delete = 1 where session_id = %s", (session_id,))
    return Result.success(msg="删除成功") if status else Result.error(msg="删除失败")


@chat_bp.route('/test', methods=['GET'])
def test():
    content = request.args.get('content')
    flag = request.args.get('flag')
    flag = True if flag == 1 else False
    openai.api_key = "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"
    chat_history = []
    messages = {"role": "user", "content": content}

    # 如果聊天历史大于0则增加历史到聊天记录中
    if len(chat_history) > 0:
        messages = chat_history.append(messages)

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[messages],
        stream=True,
    )
    while flag:
        def generate():
            # 用于拼接完整的回答
            complete_answer = ""
            for chunk in response:
                chunk_message = chunk['choices'][0]['delta']
                resp_content = chunk_message.get("content")
                # 去除首role 和 尾{}的None
                if resp_content is not None:
                    complete_answer = complete_answer + str(resp_content)
                loads = json.loads(json.dumps(chunk_message))
                chunk_data = str(loads).replace("'", '"')
                yield 'data: {}\n\n'.format(chunk_data)

            print("---complete_answer: " + str(complete_answer))
            chat_history.append({"role": "assistant", "content": complete_answer})
            print("---chat_history: " + str(chat_history))

        return Response(generate(), mimetype='text/event-stream')
    else:
        return Result.success(msg="聊天结束")
