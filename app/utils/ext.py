from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.utils.database import Base, engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 启动时执行
    print("Starting up...")
    Base.metadata.create_all(bind=engine)
    yield
    # 关闭时执行
    print("Shutting down...")
    engine.dispose()