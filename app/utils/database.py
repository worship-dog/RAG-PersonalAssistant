from sqlalchemy import create_engine, Column, String, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.config import get_config


db_config = get_config("db_config")
SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://{}:{}@{}:{}/{}".format(
    db_config.username, db_config.password, db_config.db_host, db_config.db_port, db_config.db_name
)

# 创建引擎
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_size=db_config.pool_size,  # 连接池大小
    max_overflow=db_config.max_overflow  # 最大溢出连接数
)

# 会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 模型基类
Base = declarative_base()
class BaseModel(Base):
    __abstract__ = True
    id = Column(String, primary_key=True, comment="主键uuid")
    create_time = Column(TIMESTAMP, comment="创建时间")
    update_time = Column(TIMESTAMP, comment="更新时间")

# 依赖项
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()