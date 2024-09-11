import os
from contextlib import asynccontextmanager
from http import HTTPStatus
from typing import Literal

from di import DIContainer, DI
from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Engine
from pydantic import BaseModel
from slf4py import create_logger

from apigateway.core import ApiGateway
from authority.core import Authority
from common.exception import SystemException, ErrorCode
from common.port.adapter.persistence.repository.mysql import DataBase
from middleware import MonitoringMiddleware

api_gateway = ApiGateway()
authority = Authority()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """API 起動前と終了後に実行する処理を記載する"""
    if "MySQL" in os.getenv("DI_PROFILE_ACTIVES", []):
        # データベースを構築する
        engine = create_engine(os.getenv("DATABASE_URL"), echo=os.getenv("SLF4PY_LOG_LEVEL", "DEBUG") == "DEBUG")
        DIContainer.instance().register(DI.of(Engine, {}, engine))
        DataBase.metadata.create_all(bind=engine)

    api_gateway.startup()
    authority.startup()
    yield
    api_gateway.shutdown()
    authority.shutdown()


class ErrorJson(BaseModel):
    type: Literal[*[e.name for e in ErrorCode]]
    title: str
    status: HTTPStatus
    instance: str


# TODO
# - 内部通信用トークンを全ルートに強制させる -> Middleware で 内部通信用トークンに変換し、各モジュールの Resource に渡す
# - 権限によってエンドポイントを呼び出せるのかを定義する

app = FastAPI(
    title="Backend API",
    root_path=os.getenv("OPENAPI_PREFIX"),
    lifespan=lifespan,
    responses={
        422: {
            "model": ErrorJson,
            "description": "Unprocessable Entity",
            "content": {
                "application/json": {
                    "example": {
                        "type": "COMMON_2003",
                        "title": "無効なデータです",
                        "status": 422,
                        "instance": "https://localhost:8000/health/check"
                    }
                }
            }
        }
    }
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
app.add_middleware(MonitoringMiddleware)
app.include_router(api_gateway.router)
app.include_router(authority.router)


@app.exception_handler(SystemException)
async def system_exception_handler(request: Request, exception: SystemException):
    exception.logging()
    return JSONResponse(
        status_code=exception.error_code.http_status,
        content=jsonable_encoder(
            {
                "type": exception.error_code.name,
                "title": exception.error_code.message,
                "status": exception.error_code.http_status,
                "instance": str(request.url),
            }
        ),
    )


@app.exception_handler(ValueError)
async def value_error_handler(request: Request, error: ValueError):
    logger = create_logger()
    logger.error(error)
    return JSONResponse(
        status_code=ErrorCode.COMMON_2002.http_status,
        content=jsonable_encoder({
            "type": ErrorCode.COMMON_2002.name,
            "title": ErrorCode.COMMON_2002.message,
            "status": ErrorCode.COMMON_2002.http_status,
            "instance": str(request.url)
        })
    )


@app.exception_handler(AssertionError)
async def assertion_error_handler(request: Request, error: AssertionError):
    logger = create_logger()
    logger.error(error)
    return JSONResponse(
        status_code=ErrorCode.COMMON_2002.http_status,
        content=jsonable_encoder({
            "type": ErrorCode.COMMON_2002.name,
            "title": ErrorCode.COMMON_2002.message,
            "status": ErrorCode.COMMON_2002.http_status,
            "instance": str(request.url)
        })
    )


@app.exception_handler(RequestValidationError)
async def request_validation_error_handler(request: Request, error: RequestValidationError):
    logger = create_logger()
    logger.error(error)
    return JSONResponse(
        status_code=ErrorCode.COMMON_2003.http_status,
        content=jsonable_encoder({
            "type": ErrorCode.COMMON_2003.name,
            "title": ErrorCode.COMMON_2003.message,
            "status": ErrorCode.COMMON_2003.http_status,
            "instance": str(request.url)
        })
    )


@app.exception_handler(Exception)
async def exception_handler(request: Request, error: Exception):
    logger = create_logger()
    logger.error(error)
    return JSONResponse(
        status_code=ErrorCode.COMMON_1000.http_status,
        content=jsonable_encoder({
            "type": ErrorCode.COMMON_1000.name,
            "title": ErrorCode.COMMON_1000.message,
            "status": ErrorCode.COMMON_1000.http_status,
            "instance": str(request.url)
        }),
    )
