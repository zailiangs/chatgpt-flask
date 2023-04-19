import logging
from logging.handlers import TimedRotatingFileHandler


class BaseLogger:
    def __init__(self, log_file_path):
        # 创建一个 TimedRotatingFileHandle 对象并设定相关参数
        handler = TimedRotatingFileHandler(log_file_path, when='midnight', backupCount=7)
        handler.suffix = '%Y-%m-%d'

        # 配置日志信息和格式
        logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s [%(name)s] %(message)s')
        self.logger = logging.getLogger()
        self.logger.addHandler(handler)

    def debug(self, message):
        self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)
