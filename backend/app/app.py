import os
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(
    title="Backend API",
    root_path=os.getenv("OPENAPI_PREFIX"),
    lifespan=lifespan
)
