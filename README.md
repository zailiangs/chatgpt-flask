# chatgpt-flask

<a href="https://zailiangs.com" target="_blank" >
<img src="https://img.shields.io/badge/DevelopedBy-Sun Zailiang-blue.svg?" alt=""/>
</a>

[English Version](./README_EN.md)
> 本项目为 Python 接入`OpenAI GPT-3.5`模型, 简单易用，可用于快速搭建聊天机器人。  
> 响应为`RESTful`协议，不包含页面，使用`SSE`协议对接。  
> 什么是 SSE ? [Server-Sent Events 教程](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events#event_stream_format) & 
> [Example Python code](https://github.com/openai/openai-cookbook/blob/main/examples/How_to_stream_completions.ipynb)  
> 项目中使用了 GPT-3.5 的API，需要自行申请 API Key。  
> 申请链接: [OpenAI](https://chat.openai.com)

### 需求

- Python 3.8+
- GPT-3.5 API Key
- MySQL 5.7
- Gunicorn

### 配置

1. 打开`config.py`文件，修改`OPENAI_API_KEY`为你的API Key。
2. sql文件在`sql`目录下，导入到数据库中。
3. 数据源和端口号配置在`app.py`文件中，修改为你的数据库配置与端口号。

### 使用

```shell
# 安装依赖
pip install -r requirements.txt
# 运行
gunicorn app:app --bind 0.0.0.0:port
```
