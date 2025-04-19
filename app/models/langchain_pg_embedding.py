# -*- coding: UTF-8 -*-
"""
知识嵌入表

Author: worship-dog
Email: worship76@foxmail.com>
"""

from sqlalchemy import Column, String, JSON, UUID
from pgvector.sqlalchemy import Vector

from app.utils.database import Base


class LangchainPGEmbedding(Base):
    __tablename__ = "langchain_pg_embedding"

    id = Column(String)
    collection_id = Column(UUID)
    embedding = Column(Vector)
    document = Column(String)
    cmetadata = Column(JSON)
