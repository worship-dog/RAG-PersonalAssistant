# -*- coding: UTF-8 -*-
"""
Author: worship-dog
Email: worship76@foxmail.com>
"""

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.config import ROUTER_PREFIX
from app.routers import *
from app.utils.ext import lifespan


# 初始化FastAPI应用, 并添加 lifespan 事件
app: FastAPI = FastAPI(lifespan=lifespan)

# 注册路由
app.include_router(chat_router, prefix=ROUTER_PREFIX)
app.include_router(conversation_router, prefix=ROUTER_PREFIX)
app.include_router(embeddings_router, prefix=ROUTER_PREFIX)
app.include_router(knowledge_router, prefix=ROUTER_PREFIX)
app.include_router(llm_router, prefix=ROUTER_PREFIX)
app.include_router(prompt_template_router, prefix=ROUTER_PREFIX)

# 挂载静态文件目录
app.mount("/", StaticFiles(directory="static"), name="static")
