import logging as log
import os

class Logger:
    def __init__(self):
        # folder: %LOCALAPPDATA%/sque4
        self.base_dir = os.path.join(os.environ["LOCALAPPDATA"], "sque4")

        os.makedirs(self.base_dir, exist_ok=True)

        log_path = os.path.join(self.base_dir, "debug.log")

        self.logger = log.getLogger("sque4")
        self.logger.setLevel(log.DEBUG)

        if not self.logger.handlers:

            file_handler = log.FileHandler(log_path, encoding="utf-8")
            file_handler.setLevel(log.DEBUG)

            formatter = log.Formatter(
                "%(asctime)s [%(levelname)s] %(message)s"
            )
            file_handler.setFormatter(formatter)

            self.logger.addHandler(file_handler)

    def critical(self, msg):
        self.logger.critical(msg)

    def error(self, msg):
        self.logger.error(msg)

    def warning(self, msg):
        self.logger.warning(msg)
    def info(self, msg):
        self.logger.info(msg)

