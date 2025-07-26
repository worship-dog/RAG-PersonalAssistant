# -*- coding: UTF-8 -*-
"""
大模型对话链条管理

Author: worship-dog
Email: worship76@foxmail.com>
"""


import re

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


class ConversationChainManager:
    def __init__(self):
        self.chain_dict = {}
        self.prompt_template = """
请根据以下用户提问和AI助手的回答，生成一个简洁、贴切的对话标题（不超过15字）。标题应概括核心主题，避免细节描述，尽量通用化，适合作为对话记录的标签。

用户提问：
{question}

AI回答：
{answer}

要求：
标题要简短有力，突出核心关键词。
避免使用复杂句式或标点符号。
如果是具体问题，可提炼为通用主题（如将“如何用Python爬取网页数据”概括为“Python爬虫技巧”）。

示例：
用户问：“推荐几个适合新手的Python项目？” → 标题：Python新手项目推荐
用户问：“如何缓解焦虑情绪？” → 标题：焦虑缓解方法
请直接输出标题，无需额外解释。
        """

    def _create_chain(self, llm, chain_key):
        chat_prompt_template = ChatPromptTemplate.from_messages([
            ("system", self.prompt_template)
        ])

        chain = (
            chat_prompt_template
            | llm
            | StrOutputParser()
            | self.remove_think_content
            | str.strip
        )
        self.chain_dict.setdefault(chain_key, chain)

        return chain

    def get_chain(self, llm):
        llm_name = llm.model if hasattr(llm, "model") else llm.model_name
        chain = self.chain_dict.get(llm_name)
        if chain is None:
            chain = self._create_chain(llm, llm_name)
        return chain

    @staticmethod
    def remove_think_content(answer):
        # 移除审核结果思考内容
        pattern = r"<think>.*?</think>"
        answer = re.sub(pattern, "", answer, flags=re.DOTALL)
        return answer


conversation_chain_manager = ConversationChainManager()
