import logging
import datetime
from logging.handlers import TimedRotatingFileHandler


# ��¼��
class BaseLogger:
    def __init__(self, log_file_path):
        # ����һ�� TimedRotatingFileHandle �����趨��ز���
        handler = TimedRotatingFileHandler(log_file_path, when='midnight', backupCount=7)
        # ������־�ļ��ĸ�ʽ
        handler.suffix = '%Y-%m-%d.log'

        # ������־��Ϣ�͸�ʽ
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
