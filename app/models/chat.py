# -*- coding: UTF-8 -*-
"""
聊天记录表，与对话表关联，多条记录属于一个对话

Author: worship-dog
Email: worship76@foxmail.com>
"""

from sqlalchemy import Column, String, JSON

from app.utils.database import BaseModel


class Chat(BaseModel):
    __tablename__ = "t_chat"

    conversation_id = Column(String, comment="所属对话id")
    chat_content = Column(JSON, comment="聊天内容")
