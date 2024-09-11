from __future__ import annotations

from enum import Enum

from http import HTTPStatus
from typing import Callable

from slf4py import create_logger


logger = create_logger()


class ErrorLevel(Enum):
    WARN = ("WARN", logger.warning)
    ERROR = ("ERROR", logger.error)
    CRITICAL = ("CRITICAL", logger.critical)

    def __init__(self, level: str, logging: Callable[[str], None]):
        self.level = level
        self.__logging = logging

    def to_logger(self, error_code: ErrorCode, detail: str):
        msg = "[Code] {code} [Message] {message} [Detail] {detail}".format(
            code=error_code.name, message=error_code.message, detail=detail
        )
        self.__logging(msg)


class ErrorCode(Enum):
    COMMON_1000 = ("想定外の原因エラーが発生しました", ErrorLevel.ERROR, HTTPStatus.INTERNAL_SERVER_ERROR)
    COMMON_2001 = ("アクセス拒否", ErrorLevel.WARN, HTTPStatus.FORBIDDEN)
    COMMON_2002 = ("不正なリクエストです", ErrorLevel.WARN, HTTPStatus.BAD_REQUEST)
    COMMON_2003 = ("無効なデータです", ErrorLevel.WARN, HTTPStatus.UNPROCESSABLE_ENTITY)

    def __init__(self, message: str, error_level: ErrorLevel, http_status: HTTPStatus):
        self.message = message
        self.error_level = error_level
        self.http_status = http_status

    def log(self, detail: str):
        self.error_level.to_logger(self, detail)
