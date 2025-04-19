# -*- coding: UTF-8 -*-
"""
大模型表

Author: worship-dog
Email: worship76@foxmail.com>
"""

from sqlalchemy import Column, String

from app.utils.database import BaseModel


class LLM(BaseModel):
    __tablename__ = "t_llm"

    source = Column(String, comment="大模型来源 ollama/openai/other")
    name = Column(String, comment="大模型名称")
    base_url = Column(String, comment="大模型服务地址")
    api_key = Column(String, comment="大模型API密钥")
