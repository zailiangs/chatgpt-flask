import logging
from logging.handlers import TimedRotatingFileHandler


class BaseLogger:
    def __init__(self, log_file_path):
        # ����һ�� TimedRotatingFileHandle �����趨��ز���
        handler = TimedRotatingFileHandler(log_file_path, when='midnight', backupCount=7)
        handler.suffix = '%Y-%m-%d'

        # ������־��Ϣ�͸�ʽ
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
