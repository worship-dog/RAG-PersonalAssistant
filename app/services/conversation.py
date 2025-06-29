# -*- coding: UTF-8 -*-
"""
对话服务

Author: worship-dog
Email: worship76@foxmail.com>
"""

from sqlalchemy import desc

from app.models.chat import Chat
from app.models.conversation import Conversation
from app.utils.database import Session
from app.utils.history_message import history_message_manager


class ConversationManager:
    @staticmethod
    def create_conversation(session: Session, name: str):
        """
        创建对话
        :param session: 数据库会话
        :return:
        """
        conversation = Conversation(name=name)
        session.add(conversation)
        session.commit()
        return conversation.id

    @staticmethod
    def get_conversations(session: Session):
        """
        查询对话列表
        :param session: 数据库会话
        :return:
        """
        conversations = session.query(
            Conversation.id,
            Conversation.name
        ).order_by(desc(Conversation.update_time)).all()

        return [{
            "id": conv.id,
            "name": conv.name
        } for conv in conversations]

    @staticmethod
    def update_conversation(session: Session, **kwargs):
        """
        更新对话
        :param session: 数据库会话
        :param kwargs: 可更新字段(name)
        :return:
        """
        conversation = session.query(Conversation).filter_by(id=kwargs.get('conversation_id')).first()
        if conversation:
            for key, value in kwargs.items():
                if hasattr(conversation, key):
                    setattr(conversation, key, value)
            session.commit()

    @staticmethod
    def delete_conversation(session: Session, conversation_id: str):
        """
        删除对话
        :param session: 数据库会话
        :param conversation_id: 对话ID
        :return: 如果删除成功返回True，未找到则返回False
        """
        conversation = session.query(Conversation).filter_by(id=conversation_id).first()
        if conversation:
            # 删除对话下所有聊天记录
            for chat in session.query(Chat).filter_by(conversation_id=conversation_id).all():
                session.delete(chat)
            session.delete(conversation)
            session.commit()

            # 删除redis中的历史记录
            history_message_manager.get_history_messages(conversation_id).clear()


conversation_manager = ConversationManager()
