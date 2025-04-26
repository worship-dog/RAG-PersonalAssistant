# -*- coding: UTF-8 -*-
"""
嵌入模型管理

Author: worship-dog
Email: worship76@foxmail.com>
"""

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.services import embeddings_manager
from app.utils.database import get_sync_db, SyncSessionLocal


router = APIRouter(
    tags=["embeddings"],
    dependencies=[Depends(get_sync_db)]
)


class EmbeddingCreateRequest(BaseModel):
    source: str
    name: str
    base_url: str


class EmbeddingDeleteRequest(BaseModel):
    embeddings_id: str


class EmbeddingUpdateRequest(EmbeddingCreateRequest, EmbeddingDeleteRequest):
    pass


@router.post("/embeddings")
def create_embedding(
    request: EmbeddingCreateRequest, 
    session: SyncSessionLocal = Depends(get_sync_db)
):
    """ 创建嵌入模型配置 """
    create_data = request.model_dump(exclude_unset=True)
    embeddings_manager.add_embeddings(session, **create_data)
    return {"code": 200, "msg": "success"}


@router.put("/embeddings")
def edit_embedding(
    request: EmbeddingUpdateRequest,
    session: SyncSessionLocal = Depends(get_sync_db)
):
    """
    修改嵌入模型配置
    :param request: 包含更新参数的请求体
    :param session: 数据库会话
    :return: 修改结果
    """
    update_data = request.model_dump(exclude_unset=True)
    embeddings_manager.update_embeddings(session, **update_data)
    return {"code": 200, "msg": "success"}


@router.delete("/embeddings")
def del_embedding(
    request: EmbeddingDeleteRequest,
    session: SyncSessionLocal = Depends(get_sync_db)
):
    """
    删除嵌入模型配置
    :param request: 包含删除参数的请求体
    :param session: 数据库会话
    :return: 删除结果
    """
    embeddings_manager.delete_embeddings(session, request.embeddings_id)
    return {"code": 200, "msg": "success"}


@router.get("/embeddings/list")
def get_embedding_list(session: SyncSessionLocal = Depends(get_sync_db)):
    """
    获取嵌入模型列表
    :param session: 数据库会话
    :return: 嵌入模型列表
    """
    embeddings_list = embeddings_manager.get_embeddings_list(session)
    return {"code": 200, "message": "success", "data": embeddings_list}
