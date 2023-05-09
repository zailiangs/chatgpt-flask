import json
import uuid
from datetime import datetime

import openai
from flask import request, Response, Blueprint
from flask_cors import cross_origin

import app
from common.wrapper import Logger, Result

# 一个蓝图对象
chat_bp = Blueprint('chat', __name__, url_prefix='/api')
# 初始化日志
logger = Logger('./logs/chat.log')


# AI聊天(不含上下文)
@cross_origin()
@chat_bp.route('/chat', methods=['GET'])
def chat():
    content = request.args.get('content')
    if content is None or content == "":
        return Result.error(msg="内容为空")
    openai.api_key = app.Config.OPENAI_API_KEY
    response = openai.ChatCompletion.create(
        model=app.Config.MODEL,
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


# AI聊天(含上下文)
@chat_bp.route('/chatPlus', methods=['GET'])
def chatPlus():
    content = request.args.get('content')
    session_id = request.args.get('session_id')
    if content is None or content == "":
        return Result.error(msg="内容为空")
    openai.api_key = app.Config.OPENAI_API_KEY
    chat_history = []
    # 根据session_id获取对话历史
    results = app.fetchall_sql("select question, answer from ai_dialogue where session_id = %s limit 5", (session_id,))
    if results is not None:
        for result in results:
            chat_history.append({"role": "user", "content": result[0]})
            chat_history.append({"role": "assistant", "content": result[1]})

    messages = {"role": "user", "content": content}

    # 如果聊天历史大于0则增加历史到聊天记录中
    if len(chat_history) > 0:
        chat_history.append(messages)
        messages = chat_history
    else:
        messages = [messages]
        # 否则将用户的问题前20个字重命名会话名称
        app.execute_sql("update ai_session set session_name = %s where session_id = %s", (content[:20], session_id))

    # 将聊天记录转换为json对象格式
    messages = json.loads(json.dumps(messages))

    response = openai.ChatCompletion.create(
        model=app.Config.MODEL,
        messages=messages,
        stream=True,
    )

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
        chat_history.append({"role": "assistant", "content": complete_answer})
        # 将用户的问题和AI的回答存入数据库
        app.execute_sql("insert into ai_dialogue (session_id, question, answer) values (%s, %s, %s)",
                        (session_id, content, complete_answer))

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


# 获取对话历史
@chat_bp.route('/getDialogueHistory', methods=['GET'])
def get_dialogue_history():
    session_id = request.args.get("session_id")
    results = app.fetchall_sql("select question, answer, create_time from ai_dialogue where session_id = %s order by "
                               "create_time desc", (session_id,))
    data = []
    if results is not None:
        for result in results:
            row_data = {'question': result[0], 'answer': result[1],
                        'create_time': result[2].strftime("%Y-%m-%d %H:%M:%S")}
            data.append(row_data)
    return Result.success(data=data)


@chat_bp.route('/test', methods=['GET'])
def test():
    return Result.success()
