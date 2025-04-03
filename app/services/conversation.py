# -*- coding: UTF-8 -*-
"""
对话服务

Author: worship-dog
Email: worship76@foxmail.com>
"""

from sqlalchemy import desc

from app.models import Conversation
from app.utils.database import SyncSessionLocal


def get_conversations(session: SyncSessionLocal):
    conversations = session.query(Conversation.id, Conversation.name).order_by(desc(Conversation.update_time)).all()
    rows = [{
        "conversation_id": conversation.id,
        "conversation_name": conversation.name
    } for conversation in conversations]

    return rows
