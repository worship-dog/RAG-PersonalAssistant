# -*- coding: UTF-8 -*-
"""
聊天api

Author: worship-dog
Email: worship76@foxmail.com>
"""

from fastapi import APIRouter, Depends, Request
from fastapi.responses import StreamingResponse

from app.services.chat import chat_manager

from app.utils.database import get_sync_db, get_async_db, AsyncSession, SyncSessionLocal


router = APIRouter(
    tags=["chat"]
)


@router.post("/chat")
async def astream_chat(request: Request, session: AsyncSession = Depends(get_async_db)):
    """
    SSE 流式问答
    :param request: conversation_id、chat_id、question、llm_id、prompt_template_id
    :param session: 异步数据库连接
    :return: answer_block
    """
    data = await request.json()
    return StreamingResponse(
        chat_manager.astream_generate_answer(session, **data),
        media_type="text/event-stream",  # 必须的SSE头
    )


@router.get("/chat")
def get_chat_list(request: Request, session: SyncSessionLocal = Depends(get_sync_db)):
    """
    查询聊天记录
    :param request: conversation_id
    :param session: 数据库连接
    :return: list[record]
    """
    conversation_id = request.query_params.get("conversation_id")
    data = get_chats(session, conversation_id)
    return {"code": 200, "msg": "查询成功!", "data": data}
