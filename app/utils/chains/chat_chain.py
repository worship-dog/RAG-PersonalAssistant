# -*- coding: UTF-8 -*-
"""
大模型回答链条管理

Author: worship-dog
Email: worship76@foxmail.com>
"""

import json
import hashlib

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableWithMessageHistory, RunnableParallel, RunnableLambda

from app.config import MIN_SIMILARITY
from app.utils.history_message import history_message_manager
from app.utils.vector import vector_manager


class ChatChainManager:
    def __init__(self):
        self.chain_dict = {}

    def _create_chain(self, prompt_template_info, llm, chain_key, embeddings):
        vector_store = vector_manager.get_vector(embeddings, async_mode=True)
        retriever = vector_store.as_retriever(
            search_type="similarity_score_threshold", 
            search_kwargs={"k": 6, "score_threshold": MIN_SIMILARITY}
        )

        chat_prompt_template = ChatPromptTemplate.from_messages([
            ("system", prompt_template_info["content"]),
            MessagesPlaceholder(variable_name="history"),
            ("human", "{input}")
        ])

        chain = (
            RunnableParallel({
                "input": lambda x:x["input"] ,
                "context": RunnableLambda(lambda x:x["input"]) | retriever | self.format_docs,
                "history": lambda x:x["history"]
            })
            | history_message_manager.limit_history_messages
            # | self.debug_params
            | chat_prompt_template
            # | self.debug_params
            | llm
            | StrOutputParser()
        )

        chain_with_history = RunnableWithMessageHistory(
            chain,
            lambda session_id: history_message_manager.get_history_messages(session_id),
            input_messages_key="input",
            history_messages_key="history"
        )

        self.chain_dict.setdefault(chain_key, chain_with_history)

        return chain_with_history

    def get_chain(self, prompt_template_info, llm, embeddings):
        llm_name = llm.model if hasattr(llm, "model") else llm.model_name
        # 生成提示词模板的唯一指纹
        template_fingerprint = hashlib.md5(
            json.dumps(prompt_template_info, sort_keys=True).encode('utf-8')
        ).hexdigest()[:8]  # 取8位短哈希
        chain_key = f"{llm_name}_{prompt_template_info['name']}_{template_fingerprint}"
        chain = self.chain_dict.get(chain_key)
        if chain is None:
            chain = self._create_chain(prompt_template_info, llm, chain_key, embeddings)
        return chain

    @staticmethod
    def debug_params(x):
        print(x)
        return x

    @staticmethod
    def format_docs(docs):
        doc_str = "\n\n".join([doc.page_content for doc in docs])
        return doc_str


chat_chain_manager = ChatChainManager()
