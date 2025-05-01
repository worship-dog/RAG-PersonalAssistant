# -*- coding: UTF-8 -*-
"""
聊天api

Author: worship-dog
Email: worship76@foxmail.com>
"""
from fastapi import APIRouter, Depends, Request, WebSocket

from app.services.chat import chat_manager
from app.utils.database import get_sync_db, get_async_db, AsyncSession, SyncSessionLocal


router = APIRouter(
    tags=["chat"]
)


@router.websocket("/chat/stream")
async def websocket_chat(websocket: WebSocket, session: AsyncSession = Depends(get_async_db)):
    """
    WebSocket 流式问答
    :param websocket: WebSocket连接
    :param session: 异步数据库连接
    :return: WebSocket消息流
    """
    await websocket.accept()
    
    try:
        while True:
            try:
                # 接收初始参数
                params = await websocket.receive_json()
                data = {
                    "conversation_id": params.get("conversation_id"),
                    "chat_id": params.get("chat_id"),
                    "question": params.get("question"),
                    "llm_id": params.get("llm_id"),
                    "prompt_template_id": params.get("prompt_template_id")
                }
                # 流式生成回答
                async for chunk in chat_manager.astream_generate_answer(session, **data):
                    await websocket.send_text(chunk)
            except Exception as e:
                # 仅记录错误，不发送给客户端
                print(f"WebSocket error: {e}")
                break
    finally:
        # 确保连接关闭
        try:
            await websocket.close()
        except Exception:
            pass


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
