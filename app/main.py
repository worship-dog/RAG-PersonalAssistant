# -*- coding: UTF-8 -*-
"""
Author: worship-dog
Email: worship76@foxmail.com>
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.routers import *
from app.utils.ext import lifespan


app: FastAPI = FastAPI(lifespan=lifespan)

# 配置CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许的源，可以替换为特定域名，例如 ["http://localhost:8080"]
    allow_credentials=True,
    allow_methods=["*"],  # 允许的请求方法（GET, POST, PUT, DELETE等）
    allow_headers=["*"],  # 允许的请求头
)

# 注册路由
app.include_router(auth_router)
app.include_router(chat_router)
app.include_router(collection_router)
app.include_router(conversation_router)
app.include_router(embeddings_router)
app.include_router(knowledge_router)
app.include_router(llm_router)
app.include_router(prompt_template_router)
app.include_router(record_router)

# 挂载静态文件目录
app.mount("/", StaticFiles(directory="static"), name="static")
