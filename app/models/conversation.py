# -*- coding: UTF-8 -*-
"""
对话表，与记录表关联，每个对话包含多条记录

Author: worship-dog
Email: worship76@foxmail.com>
"""

from sqlalchemy import Column, String, JSON

from app.utils.database import BaseModel


class Conversation(BaseModel):
    __tablename__ = "t_conversation"

    name = Column(String, comment="对话名")
