# -*- coding: UTF-8 -*-
"""
知识表，与知识库表关联，多条知识属于一个知识库

Author: worship-dog
Email: worship76@foxmail.com>
"""

from sqlalchemy import Column, String, JSON

from app.utils.database import BaseModel


class Knowledge(BaseModel):
    __tablename__ = "t_knowledge"

    name = Column(String, comment="知识名")
    knowledge = Column(JSON, comment="知识内容")
    index = Column(String, comment="页码")
