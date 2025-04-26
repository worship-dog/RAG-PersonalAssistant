# -*- coding: UTF-8 -*-
"""
知识库管理

Author: worship-dog
Email: worship76@foxmail.com>
"""

from fastapi import APIRouter

from app.config import user_name, avatar


router = APIRouter(tags=["auth"])


@router.post("/auth/login")
def login():
    return {"code": 200, "msg": "success", "data": {"token": "token"}}


@router.get("/auth/user/info")
def get_user_info():
    return {"code": 200, "msg": "success", "data": {
        "roles": ["admin"],
        "name": user_name,
        "avatar": avatar,
    }}
