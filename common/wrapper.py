import datetime
import logging
from logging.handlers import TimedRotatingFileHandler


# 封装返回结果
class Result:
    @staticmethod
    def success(code=200, msg="SUCCESS", data=None):
        return {"code": code, "msg": msg, "data": data}

    @staticmethod
    def error(code=400, msg="ERROR", data=None):
        return {"code": code, "msg": msg, "data": data}


# 封装日志操作
class Logger:
    def __init__(self, log_file_path):
        # 创建一个 TimedRotatingFileHandle 对象并设定相关参数
        handler = TimedRotatingFileHandler(log_file_path, when='midnight', backupCount=7)
        # 设置日志文件的格式
        handler.suffix = '%Y-%m-%d.log'

        # 配置日志信息和格式
        logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s [%(name)s] %(message)s')
        self.logger = logging.getLogger()
        self.logger.addHandler(handler)

    def debug(self, message):
        time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.logger.debug(time + " [DEBUG] " + message)

    def info(self, message):
        time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.logger.info(time + " [INFO] " + message)

    def warning(self, message):
        time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.logger.warning(time + " [WARNING] " + message)

    def error(self, message):
        time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.logger.error(time + " [ERROR] " + message)
