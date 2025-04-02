# -*- coding: UTF-8 -*-
"""
初始化大模型

Author: worship-dog
Email: worship76@foxmail.com>
"""

from langchain_ollama import OllamaLLM

from app.config import get_config


llm_source_dict = {"ollama": OllamaLLM, "openai": OllamaLLM}

# 载入大语言模型
llm_config = get_config("llm_config")
llm_class = llm_source_dict[llm_config.source]
llm = llm_class(model=llm_config.model, base_url=llm_config.base_url)
