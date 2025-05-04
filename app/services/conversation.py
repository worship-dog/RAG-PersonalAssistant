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


class ConversationManager:
    def create_conversation(self, session: Session, name: str):  # 修改参数
        conversation = Conversation(name=name)
        session.add(conversation)
        session.commit()
        return conversation.id

    def get_conversations(self, session: Session):
        conversations = session.query(
            Conversation.id,
            Conversation.name  # 只返回 name 字段
        ).order_by(desc(Conversation.update_time)).all()

        return [{
            "id": conv.id,
            "name": conv.name
        } for conv in conversations]

    def update_conversation(self, session: Session, **kwargs):
        """
        更新对话
        :param session: 数据库会话
        :param kwargs: 可更新字段(name)
        :return:
        """
        conversation = session.query(Conversation).filter(
            Conversation.id == kwargs.get('conversation_id')
        ).first()
        if conversation:
            for key, value in kwargs.items():
                if hasattr(conversation, key):
                    setattr(conversation, key, value)
            session.commit()

    def delete_conversation(self, session: Session, conversation_id: str):
        """
        删除对话
        :param session: 数据库会话
        :param conversation_id: 对话ID
        :return: 如果删除成功返回True，未找到则返回False
        """
        conversation = session.query(Conversation).filter(
            Conversation.id == conversation_id
        ).first()
        if conversation:
            # 删除对话下所有聊天记录
            for chat in session.query(Chat).filter(Chat.conversation_id == conversation_id).all():
                session.delete(chat)
            session.delete(conversation)
            session.commit()
            return True
        return False


conversation_manager = ConversationManager()
