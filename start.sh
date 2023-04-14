#!/bin/bash

# 激活虚拟环境
source venv/bin/activate

# 设置 Flask 应用程序变量
export FLASK_APP=app.py

# 启动 Gunicorn
gunicorn --bind 0.0.0.0:8000 wsgi:app
