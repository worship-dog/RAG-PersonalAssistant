# -*- coding: UTF-8 -*-
"""
聊天api

Author: worship-dog
Email: worship76@foxmail.com>
"""
from collections import defaultdict
import asyncio
import json

from fastapi import APIRouter, Depends, Request
from sse_starlette import EventSourceResponse, ServerSentEvent

from app.services.chat import chat_manager
from app.utils.database import async_db_scope, get_sync_db, Session
from app.utils.history_message import history_message_manager
from app.utils.timer import timer_dict, Timer


chat_queues = defaultdict(asyncio.Queue)  # sse 客户端

router = APIRouter(
    tags=["chat"]
)


@router.post("/chat/sse")
async def sse_chat(request: Request):
    """
    SSE 流式问答
    :param request: 
        client_id, 
        conversation_id, 
        chat_id, 
        question, 
        llm_id, 
        prompt_template_id
    :return: SSE消息流
    """
    data = await request.json()

    # 初始化事件队列
    chat_key = f"{data.get('client_id')}_{data.get('conversation_id')}"
    if chat_key not in chat_queues:
        chat_queues[chat_key] = asyncio.Queue()

    async def generate_answer():
        # 记录回答、思考耗时
        answer = ""
        timer_dict.setdefault(chat_key, Timer())
        think_time = 0
        chat_queue = chat_queues[chat_key]
        await chat_queue.put({"status": "start"})

        async with async_db_scope() as session:
            try:
                # 流式生成回答
                async for chunk in chat_manager.astream_generate_answer(
                        timer_dict[chat_key], session, **data):
                    await chat_queue.put({"status": "message", "chunk": chunk})
                    answer += chunk
            except Exception as e:
                print(e)
                await chat_queue.put({"status": "error", "data": str(e)})

            await chat_queue.put({"status": "finish"})
            await chat_queue.put({"status": "close"})

            # 保存回答
            await chat_manager.save_chat(session, answer, think_time, **data)

    asyncio.create_task(generate_answer())

    async def event_generator():
        try:
            while True:
                # 获取事件（支持超时检测）
                try:
                    raw_data: dict = await asyncio.wait_for(
                        chat_queues[chat_key].get(), timeout=10)
                    event = raw_data.pop("status")
                    if event == "close":  # 检测到结束标志
                        break
                    yield ServerSentEvent(
                        data=json.dumps(raw_data, ensure_ascii=False),
                        event=event  # start | message | finish | close
                    )
                except asyncio.TimeoutError:
                    yield {"event": "ping"}  # 发送心跳包保持连接
        except asyncio.CancelledError:
            # 客户端断开连接时触发清理
            chat_queues.pop(chat_key, None)

    return EventSourceResponse(event_generator())


@router.get("/chat/list")
def get_chat_list(request: Request, session: Session = Depends(get_sync_db)):
    """
    查询聊天记录
    :param request: conversation_id
    :param session: 数据库连接
    :return: list[record]
    """
    conversation_id = request.query_params.get("conversation_id")
    data = chat_manager.get_chats(session, conversation_id)
    history_message_manager.add_history_messages(conversation_id, data)
    return {"code": 200, "msg": "查询成功!", "data": data}
