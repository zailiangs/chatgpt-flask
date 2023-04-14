import openai
import time
import json
from flask import request, Response, Blueprint
from flask_cors import CORS, cross_origin

# 一个蓝图对象
ChatGPT = Blueprint('chat', __name__)
CORS(ChatGPT, resources={r"/*": {"origins": "*"}})


@cross_origin()
@ChatGPT.route('/chat', methods=['POST'])
def chat():
    # 获取POST请求中的JSON数据参数
    content = request.get_json()['content']
    openai.api_key = "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"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": content}
        ],
        stream=True,
    )

    def generate():
        # 开始时间
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
        print(f"完全响应请求: {end_time:.2f} 秒")

    return Response(generate(), mimetype='text/event-stream')


@cross_origin()
@ChatGPT.route('/sse', methods=['GET', 'POST'])
def sse():
    def event_stream():
        data_list = [{"role": "assistant"}, {"content": "你好"}, {"content": "!"}, {"content": "有"}, {"content": "什么"},
                     {"content": "可以"}, {"content": "帮助"}, {"content": "您"}, {"content": "的"}, {"content": "吗"}, {}]
        for data in data_list:
            data_replace = str(data).replace("'", "\"")
            yield 'data: {}\n\n'.format(data_replace)

    return Response(event_stream(), mimetype='text/event-stream')
