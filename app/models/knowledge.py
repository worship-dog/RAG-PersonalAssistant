# -*- coding: UTF-8 -*-
"""
知识库文件表

Author: worship-dog
Email: worship76@foxmail.com>
"""

from sqlalchemy import Column, String, JSON

from app.utils.database import BaseModel


class Knowledge(BaseModel):
    __tablename__ = "t_knowledge"

    collection_id = Column(String, comment="所属知识库id")
    name = Column(String, comment="知识名")
    knowledge = Column(JSON, comment="知识内容")
    index = Column(String, comment="页码")
