# -*- coding: UTF-8 -*-
"""
数据库连接

Author: worship-dog
Email: worship76@foxmail.com>
"""
from contextlib import contextmanager, asynccontextmanager
from datetime import datetime
import uuid

from fastapi import HTTPException
from loguru import logger
from sqlalchemy import create_engine, Column, String, TIMESTAMP
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from app.config import get_config


# 模型基类
Base = declarative_base()
class BaseModel(Base):
    __abstract__ = True
    id = Column(String, primary_key=True, comment="主键uuid")
    create_time = Column(TIMESTAMP, default=datetime.now, comment="创建时间")
    update_time = Column(TIMESTAMP, default=datetime.now, onupdate=datetime.now, comment="更新时间")

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            if k in ["id", "create_time", "update_time"]:
                continue
            if hasattr(self, k):
                setattr(self, k ,v)
        self.id = str(uuid.uuid4())


db_config = get_config("db_config")

# 创建同步引擎
SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://{}:{}@{}:{}/{}".format(
    db_config.username, db_config.password, db_config.db_host, db_config.db_port, db_config.db_name
)
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_size=db_config.pool_size,  # 连接池大小
    max_overflow=db_config.max_overflow  # 最大溢出连接数
)

# 同步会话工厂
SyncSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=Session)


@contextmanager
def db_scope():
    db = SyncSessionLocal()
    try:
        db.begin()  # 启动事务
        yield db
        db.commit()  # 提交事务
    except Exception as e:
        logger.error(e)
        db.rollback()  # 回滚
        raise HTTPException(status_code=500, detail=e.args[0])
    finally:
        db.close()

# 同步数据库连接依赖项
def get_sync_db():
    with db_scope() as db:
        yield db


# 创建异步引擎
ASYNC_SQLALCHEMY_DATABASE_URL = "postgresql+asyncpg://{}:{}@{}:{}/{}".format(
    db_config.username, db_config.password, db_config.db_host, db_config.db_port, db_config.db_name
)
async_engine = create_async_engine(ASYNC_SQLALCHEMY_DATABASE_URL)

# 异步会话工厂
AsyncSessionLocal = async_sessionmaker(bind=async_engine, class_=AsyncSession, expire_on_commit=False)


# 异步数据库连接依赖项
@asynccontextmanager
async def async_db_scope():
    db = AsyncSessionLocal()
    try:
        await db.begin()  # 开始事务
        yield db
        await db.commit()  # 提交事务
    except Exception as e:
        logger.error(e)
        await db.rollback()  # 回滚
        raise HTTPException(status_code=500, detail=e)
    finally:
        await db.close()


async def get_async_db():
    async with async_db_scope() as db:
        yield db
