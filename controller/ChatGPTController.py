import json
import time

import openai
from flask import request, Response, Blueprint
from flask_cors import cross_origin

from baseLogger import BaseLogger

# 一个蓝图对象
ChatGPT = Blueprint('chat', __name__)
# 初始化日志
logger = BaseLogger('./logs/app.log')


@cross_origin()
@ChatGPT.route('/chat', methods=['GET'])
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
        start_time = time.time()
        # 流式响应
        for chunk in response:
            chunk_message = chunk['choices'][0]['delta']
            # 使用json包将字典转换为JSON格式的字符串
            loads = json.loads(json.dumps(chunk_message))
            # 将单引号替换为双引号
            chunk_data = str(loads).replace("'", "\"")
            # 返回响应
            yield 'data: {}\n\n'.format(chunk_data)

        end_time = time.time() - start_time
        logger.info(f"完全响应请求: {end_time:.2f} 秒")

    return Response(generate(), mimetype='text/event-stream')


@cross_origin()
@ChatGPT.route('/sse', methods=['GET'])
def sse():
    content = request.args.get("content")
    logger.info("--------------------sse api call")

    def event_stream():
        data_list = [{"role": "assistant"}, {"content": "你好"}, {"content": "!"}, {"content": "有"}, {"content": "什么"},
                     {"content": "可以"}, {"content": "帮助"}, {"content": "您"}, {"content": "的"}, {"content": "吗?"},
                     {"content": " 内容测试词: "}, {"content": content}, {}]
        for data in data_list:
            data_replace = str(data).replace("'", '"')
            yield 'data: {}\n\n'.format(data_replace)

    return Response(event_stream(), mimetype='text/event-stream')
