# -*- coding: UTF-8 -*-
"""
初始化大模型

Author: worship-dog
Email: worship76@foxmail.com>
"""

from langchain_ollama import OllamaLLM


llm_source_dict = {"ollama": OllamaLLM, "openai": OllamaLLM}


# 载入大语言模型
def get_llm(source, model, base_url):
    llm_class = llm_source_dict[source]
    llm = llm_class(model=model, base_url=base_url)
    return llm
