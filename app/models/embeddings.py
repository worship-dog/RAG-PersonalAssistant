# -*- coding: UTF-8 -*-
"""
嵌入模型表

Author: worship-dog
Email: worship76@foxmail.com>
"""

from sqlalchemy import Column, String

from app.utils.database import BaseModel


class Embeddings(BaseModel):
    __tablename__ = "t_embeddings"

    source = Column(String, comment="嵌入模型来源 ollama/openai/other")
    name = Column(String, comment="嵌入模型名称")
    base_url = Column(String, comment="嵌入模型服务地址")
