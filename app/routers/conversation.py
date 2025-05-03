# -*- coding: UTF-8 -*-
"""
知识库管理

Author: worship-dog
Email: worship76@foxmail.com>
"""

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.services import conversation_manager
from app.utils.database import get_sync_db, SyncSessionLocal


router = APIRouter(
    tags=["collection"],
    dependencies=[Depends(get_sync_db)]
)


class ConversationCreateRequest(BaseModel):
    name: str  # 修改字段名称为 name


class ConversationDeleteRequest(BaseModel):
    conversation_id: str


class ConversationUpdateRequest(ConversationCreateRequest, ConversationDeleteRequest):
    pass


@router.post("/conversation")
def create_conversation(
    request: ConversationCreateRequest,
    session: SyncSessionLocal = Depends(get_sync_db)
):
    """ 创建对话 """
    create_data = request.model_dump(exclude_unset=True)
    conversation_id = conversation_manager.create_conversation(session, **create_data)
    return {"code": 200, "msg": "success", "data": {"conversation_id": conversation_id}}

@router.put("/conversation")
def edit_conversation(
    request: ConversationUpdateRequest,
    session: SyncSessionLocal = Depends(get_sync_db)
):
    """
    更新对话
    :param request: 包含更新参数的请求体
    :param session: 数据库会话
    :return: 更新结果
    """
    update_data = request.model_dump(exclude_unset=True)
    conversation_manager.update_conversation(session, **update_data)
    return {"code": 200, "msg": "success"}

@router.delete("/conversation")
def del_conversation(
    request: ConversationDeleteRequest,
    session: SyncSessionLocal = Depends(get_sync_db)
):
    """
    删除对话
    :param request: 包含删除参数的请求体
    :param session: 数据库会话
    :return: 删除结果
    """
    conversation_manager.delete_conversation(session, request.conversation_id)
    return {"code": 200, "msg": "success"}


@router.get("/conversation")
def get_conversation():
    pass


@router.get("/conversation/list")
def get_conversation_list(session: SyncSessionLocal = Depends(get_sync_db)):
    data = conversation_manager.get_conversations(session)
    return {"code": 200, "msg": "success", "data": data}
