# -*- coding: UTF-8 -*-
"""
历史聊天记录管理

Author: worship-dog
Email: worship76@foxmail.com>
"""
from langchain_core.messages import AIMessage, HumanMessage
from langchain_community.chat_message_histories import RedisChatMessageHistory

from app.config import get_config, HISTORY_EXPIRE_TIME, HISTORY_MAX_LENGTH


class HistoryMessageManager:
    def __init__(self):
        redis_config = get_config("redis_config")
        self.redis_url = f"redis://{redis_config.host}:{redis_config.port}/{redis_config.db}"
        self.history_dict = {}

    # 从Redis查询历史聊天记录
    def get_history_messages(self, session_id) -> RedisChatMessageHistory:
        if session_id not in self.history_dict:
            self.history_dict[session_id] = RedisChatMessageHistory(
                session_id, self.redis_url, ttl=HISTORY_EXPIRE_TIME)
        return self.history_dict[session_id]

    # 手动添加历史聊天记录
    def add_history_messages(self, session_id, messages):
        history_messages: RedisChatMessageHistory = self.get_history_messages(session_id)
        if len(history_messages.messages) == len(messages) * 2:
            return
        elif len(history_messages.messages) < HISTORY_MAX_LENGTH:
            history_messages.clear()
            for message in messages:
                for ai_message in message["ai"]:
                    history_messages.add_message(HumanMessage(message["human"]))
                    history_messages.add_message(AIMessage(ai_message["answer"]))

    # 限制历史聊天记录长度
    @staticmethod
    def limit_history_messages(data):
        if len(data["history"]) > HISTORY_MAX_LENGTH:
            data["history"] = data["history"][-HISTORY_MAX_LENGTH:]
        return data


history_message_manager = HistoryMessageManager()
