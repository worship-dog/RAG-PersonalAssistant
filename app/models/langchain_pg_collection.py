# -*- coding: UTF-8 -*-
"""
知识库表，与知识表关联，每个知识库包含多条知识

Author: worship-dog
Email: worship76@foxmail.com>
"""

from sqlalchemy import Column, String, JSON, UUID

from app.utils.database import Base


class LangchainPGCollection(Base):
    __tablename__ = "langchain_pg_collection"

    uuid = Column(UUID, primary_key=True)
    name = Column(String)
    cmetadata = Column(JSON)
