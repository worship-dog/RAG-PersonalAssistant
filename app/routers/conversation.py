# -*- coding: UTF-8 -*-
"""
知识库管理

Author: worship-dog
Email: worship76@foxmail.com>
"""

from fastapi import APIRouter, Depends

from app.services.conversation import get_conversations
from app.utils.database import get_sync_db, SyncSessionLocal


router = APIRouter(
    tags=["conversation"],
    dependencies=[Depends(get_sync_db)]
)


@router.post("/conversation")
def create_conversation():
    pass


@router.get("/conversation")
def get_conversation():
    pass


@router.put("/conversation")
def edit_conversation():
    pass


@router.delete("/conversation")
def del_conversation():
    pass


@router.get("/conversation/list")
def get_conversation_list(session: SyncSessionLocal = Depends(get_sync_db)):
    data = get_conversations(session)
    return {"code": 200, "msg": "查询成功!", "data": data}
