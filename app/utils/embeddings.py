# -*- coding: UTF-8 -*-
"""
初始化嵌入模型

Author: worship-dog
Email: worship76@foxmail.com>
"""

from langchain_ollama import OllamaEmbeddings


embeddings_source_dict = {"ollama": OllamaEmbeddings, "openai": OllamaEmbeddings}


# 载入嵌入模型
def get_embeddings(source, model, base_url):
    embeddings_class = embeddings_source_dict[source]
    embeddings = embeddings_class(model=model, base_url=base_url)
    return embeddings
