# -*- coding: UTF-8 -*-
"""
Author: worship-dog
Email: worship76@foxmail.com>
"""

from fastapi import FastAPI

from app.routers import collection_router
from app.utils.ext import lifespan


app = FastAPI(lifespan=lifespan)
app.include_router(collection_router)
