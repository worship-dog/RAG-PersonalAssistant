# -*- coding: UTF-8 -*-
"""
提示词模板表

Author: worship-dog
Email: worship76@foxmail.com>
"""

from sqlalchemy import Column, String, Text

from app.utils.database import BaseModel


class PromptTemplate(BaseModel):
    __tablename__ = "t_prompt_template"

    name = Column(String, comment="提示词模板名称")
    content = Column(Text, comment="提示词模板内容")
