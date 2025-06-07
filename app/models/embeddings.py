# -*- coding: UTF-8 -*-
"""
嵌入模型表

Author: worship-dog
Email: worship76@foxmail.com>
"""

from sqlalchemy import Column, String, Boolean
from langchain_ollama import OllamaEmbeddings

from app.utils.database import BaseModel


class Embeddings(BaseModel):
    __tablename__ = "t_embeddings"

    source = Column(String, comment="嵌入模型来源 ollama/openai/other")
    name = Column(String, comment="嵌入模型名称")
    base_url = Column(String, comment="嵌入模型服务地址")
    default = Column(Boolean, comment="是否为默认项")

    # 初始化嵌入模型
    def init(self):
        embeddings_source_dict = {"ollama": OllamaEmbeddings, "openai": OllamaEmbeddings}
        embeddings_class = embeddings_source_dict[str(self.source)]
        embeddings = embeddings_class(model=self.name, base_url=self.base_url)
        return embeddings
