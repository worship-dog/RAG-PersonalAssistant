# -*- coding: UTF-8 -*-
"""
聊天api

Author: worship-dog
Email: worship76@foxmail.com>
"""
from collections import defaultdict
import asyncio
import json

from fastapi import APIRouter, Depends, Request, WebSocket
from sse_starlette import EventSourceResponse, ServerSentEvent

from app.services.chat import chat_manager
from app.utils.database import get_sync_db, get_async_db, AsyncSession, Session
from app.utils.timer import timer_dict, Timer


client_queues = defaultdict(asyncio.Queue)  # sse 客户端

router = APIRouter(
    tags=["chat"]
)


@router.post("/chat/sse")
async def sse_chat(request: Request, session: AsyncSession = Depends(get_async_db)):
    """
    SSE 流式问答
    :param request: conversation_id, chat_id, question, llm_id, prompt_template_id
    :param session: 异步数据库连接
    :return: SSE消息流
    """
    answer = ""
    session_id = None
    client_id = ""

    # 初始化事件队列
    if client_id not in client_queues:
        client_queues[client_id] = asyncio.Queue()

    async def generate_answer():
        await client_queues[client_id].put({"status": "start"})
        # 流式生成回答
        async for chunk in chat_manager.astream_generate_answer(timer_dict[session_id], session, **data):
            await client_queues[client_id].put({"status": "answering", "chunk": chunk})
        await client_queues[client_id].put({"status": "end"})

    asyncio.create_task(generate_answer())

    async def event_generator():
        try:
            while True:
                # 获取事件（支持超时检测）
                try:
                    raw_data = await asyncio.wait_for(client_queues[client_id].get(), timeout=10)
                    if raw_data is None:  # 检测到结束标志
                        break
                    yield ServerSentEvent(
                        data=json.dumps(raw_data),  # data必须为字符串
                        event=raw_data["status"]  # checking  | complete | failed
                    )
                except asyncio.TimeoutError:
                    yield {"event": "ping"}  # 发送心跳包保持连接
        except asyncio.CancelledError:
            # 客户端断开连接时触发清理
            client_queues.pop(client_id, None)

    return EventSourceResponse(event_generator())
    

@router.websocket("/chat/stream")
async def websocket_chat(websocket: WebSocket, session: AsyncSession = Depends(get_async_db)):
    """
    WebSocket 流式问答
    :param websocket: WebSocket连接
    :param session: 异步数据库连接
    :return: WebSocket消息流
    """
    await websocket.accept()
    session_id = None
    try:
        while True:
            # 初始化回答
            answer = ""
            # 记录思考耗时
            session_id = websocket.client.host
            timer_dict.setdefault(session_id, Timer())
            think_time = 0

            # 接收初始参数
            params = await websocket.receive_json()
            data = {
                "conversation_id": params.get("conversation_id"),
                "chat_id": params.get("chat_id"),
                "question": params.get("question"),
                "llm_id": params.get("llm_id"),
                "prompt_template_id": params.get("prompt_template_id")
            }

            # 保存问题
            try:
                # 提问时，先保存问题内容，解决用户在回答过程中切换到其他对话后 又切换回来 看不到问题的bug
                if not data.get("chat_id"):
                    data["chat_id"] = await chat_manager.save_chat(session, "", think_time, **data)
            except Exception as e:
                print(f"DB错误: {str(e)}")
                break

            # 流式生成回答
            async for chunk in chat_manager.astream_generate_answer(timer_dict[session_id], session, **data):
                answer += chunk
                await websocket.send_json({"chunk": chunk, "conversation_id": params.get("conversation_id")})
                # 记录耗时
                if timer_dict[session_id].end_timer(chunk):
                    think_time = timer_dict[session_id].elapsed
            await websocket.send_text("@@@end@@@")  #发送结束标识

            # 保存回答
            try:
                await chat_manager.save_chat(session, answer, think_time, **data)
            except Exception as e:
                print(f"DB错误: {str(e)}")
                break

    except Exception as e:
        print(f"Websocket错误: {str(e)}")
    finally:
        try:
            await websocket.close()
        except Exception as e:
            print(f"关闭WebSocket连接时出错: {str(e)}")
            # 不再抛出异常
        if timer_dict.get(session_id):
            del timer_dict[session_id]


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
    return {"code": 200, "msg": "查询成功!", "data": data}
