# -*- coding: UTF-8 -*-
"""
Author: worship-dog
Email: worship76@foxmail.com>
"""

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse

from app.routers import *
from app.utils.ext import lifespan


app: FastAPI = FastAPI(lifespan=lifespan)

app.include_router(chat_router)
app.include_router(collection_router)
app.include_router(conversation_router)
app.include_router(knowledge_router)
app.include_router(record_router)

# 挂载静态文件目录
app.mount("/", StaticFiles(directory="static"), name="static")


# @app.get("/", response_class=HTMLResponse)
# async def read_index(request: Request):
#     # 返回index.html文件的内容
#     return FileResponse("static/index.html")
