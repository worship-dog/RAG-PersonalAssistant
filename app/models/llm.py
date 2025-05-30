# -*- coding: UTF-8 -*-
"""
大模型表

Author: worship-dog
Email: worship76@foxmail.com>
"""

from typing import Union

from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI
from sqlalchemy import Column, String

from app.utils.database import BaseModel


class LLM(BaseModel):
    __tablename__ = "t_llm"

    source = Column(String, comment="大模型来源 ollama/openai/other")
    name = Column(String, comment="大模型名称")
    base_url = Column(String, comment="大模型服务地址")
    api_key = Column(String, comment="大模型API密钥")

    # 初始化大语言模型
    def init(self) -> Union[ChatOpenAI, ChatOllama]:
        source_model_dict = {
            "ollama": ChatOllama,
            "openai": ChatOpenAI,
            "other": ChatOpenAI
        }
        chat_model = source_model_dict[str(self.source)]
        llm = chat_model(
            model=self.name,
            base_url=self.base_url,
            api_key=self.api_key
        )
        return llm
