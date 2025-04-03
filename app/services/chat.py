# -*- coding: UTF-8 -*-
"""
聊天服务

Author: worship-dog
Email: worship76@foxmail.com>
"""

import json

from app.models import Chat, Conversation
from app.utils.llm import llm
from app.utils.timer import timer_dict, Timer


async def async_save_chat(session, conversation_id, question, think_time, full_response):
    # 异步存储回答内容
    if not conversation_id:
        # 不存在conversation_id是，代表新对话，自动创建conversation
        conversation = Conversation(name="新对话")  # TODO: 新对话命名
        session.add(conversation)
        conversation_id = conversation.id

    # 创建聊天记录
    chat_content = json.dumps({
        "question": question,
        "think_time": think_time,
        "answer": "".join(full_response)
    }, ensure_ascii=False)
    session.add(Chat(
        conversation_id=conversation_id,
        chat_content=chat_content
    ))


async def generate_answer(session, conversation_id, chat_id, question):
    # 计时思考时长
    think_time = 0
    # 初始化此次chat的计时器
    timer_dict.setdefault(chat_id, Timer())
    timer = timer_dict[chat_id]
    # 开始计时
    timer.start_timer()

    full_response = []  # 记录完整回答
    # TODO: 1.知识库相似检索；2.历史记录上下文
    try:
        async for chunk in llm.astream(question):  # 使用astream获取流式响应
            if timer.end_timer(chunk):  # 验证是否思考结束
                think_time = timer.elapsed

            full_response.append(chunk)  # 添加回答块
            yield f"chat_id: {chat_id}\ndata: {chunk}\n\n"  # 以SSE格式返回回答
    except Exception as e:
        print(f"Unknown Error: {e}")
    finally:
        if full_response:
            await async_save_chat(session, conversation_id, question, think_time, full_response)

    # 销毁计时器
    if chat_id in timer_dict:
        del timer_dict[chat_id]


def get_chats(session, conversation_id):
    def analysis_chat_content(chat_content):
        # 解析聊天记录
        chat_content = json.loads(chat_content)
        return chat_content

    # 查询聊天记录
    chat_list = session.query(
        Chat.id, Chat.chat_content
    ).filter(Chat.conversation_id == conversation_id).order_by(Chat.create_time).all()

    rows = [{"chat_id": chat.id, "chat_content": analysis_chat_content(chat.chat_content)} for chat in chat_list]
    return rows