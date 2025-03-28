from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://user:password@localhost:5432/dbname"

# 创建引擎
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_size=10,  # 连接池大小
    max_overflow=20  # 最大溢出连接数
)

# 会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 模型基类
Base = declarative_base()

# 依赖项
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()