# -*- coding: UTF-8 -*-
"""
记录表，与对话表关联，多条记录属于一个对话

Author: worship-dog
Email: worship76@foxmail.com>
"""

from sqlalchemy import Column, String, JSON

from app.utils.database import BaseModel


class Record(BaseModel):
    __tablename__ = "t_record"

    conversation_id = Column(String, comment="所属对话id")
