import os
import logging

from aiohttp.abc import AbstractAccessLogger
from config import Config


class AccessLogger(AbstractAccessLogger):
    def __init__(self, logger: logging.Logger, log_format: str):
        super(AccessLogger, self).__init__(logger, log_format)
        if not os.path.exists(Config.ERROR_LOG_FOLDER):
            os.mkdir(Config.ERROR_LOG_FOLDER)
        logging.basicConfig(filename=Config.ERROR_LOG_FILE, filemode='a', level=logging.ERROR)

    def log(self, request, response, time):
        if response.status in range(500, 520):
            self.logger.error(f'{request.remote} '
                              f'"{request.method} {request.path} '
                              f'done in {time}s: {response.status}')
