import os
from contextlib import asynccontextmanager
from http import HTTPStatus

from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from slf4py import create_logger
from starlette.middleware.cors import CORSMiddleware

from apigateway.port.adapter.resource import APIGatewayResource
from common.exception import SystemException


@asynccontextmanager
async def lifespan(app: FastAPI):
    """API 起動前と終了後に実行する処理を記載する"""
    yield


# TODO
# 2. 全リクエストで Sentry / New Relic へのロギングを行う
# 3. 認可処理を全ルートに強制させる
# 4. DI処理を各モジュールで行えるようにする


class ErrorJson(BaseModel):
    type: str
    title: str
    status: HTTPStatus
    instance: str


app = FastAPI(
    title="Backend API",
    root_path=os.getenv("OPENAPI_PREFIX"),
    lifespan=lifespan,
    responses={
        422: {"model": ErrorJson, "description": "Unprocessable Entity"}
    }
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
app.include_router(APIGatewayResource().router)


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
        status_code=400,
        content=jsonable_encoder(
            {"type": "CLIENT_2001", "title": "不正なリクエストです", "status": 400, "instance": str(request.url)}
        )
    )


@app.exception_handler(AssertionError)
async def assertion_error_handler(request: Request, error: AssertionError):
    logger = create_logger()
    logger.error(error)
    return JSONResponse(
        status_code=400,
        content=jsonable_encoder(
            {"type": "CLIENT_2002", "title": "不正なリクエストです", "status": 400, "instance": str(request.url)}
        ),
    )


@app.exception_handler(RequestValidationError)
async def request_validation_error_handler(request: Request, error: RequestValidationError):
    logger = create_logger()
    logger.error(error)
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder(
            {"type": "CLIENT_2003", "title": "無効なデータです", "status": 422, "instance": str(request.url)}
        )
    )


@app.exception_handler(Exception)
async def exception_handler(request: Request, error: Exception):
    logger = create_logger()
    logger.error(error)
    return JSONResponse(
        status_code=500,
        content=jsonable_encoder(
            {"type": "CLIENT_1000", "title": "エラーが発生しました", "status": 500, "instance": str(request.url)}
        ),
    )
