# -*- coding: UTF-8 -*-
"""
嵌入模型管理

Author: worship-dog
Email: worship76@foxmail.com>
"""

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.utils.database import get_sync_db, SyncSessionLocal
from app.services.embeddings import embedding_manager


router = APIRouter(
    tags=["embeddings"],
    dependencies=[Depends(get_sync_db)]
)


class EmbeddingRequest(BaseModel):
    source: str
    name: str
    base_url: str


@router.post("/embeddings")
def create_embedding(
    request: EmbeddingRequest, 
    session: SyncSessionLocal = Depends(get_sync_db)
):
    """
    创建嵌入模型配置
    :param request: 包含创建参数的请求体
    :param session: 数据库会话
    :return: 创建结果
    """
    embedding_manager.add_embedding(
        session,
        source=request.source,
        name=request.name,
        base_url=request.base_url
    )
    return {"code": 200, "msg": "success"}


@router.put("/embeddings")
def edit_embedding(
    request: EmbeddingRequest,
    session: SyncSessionLocal = Depends(get_sync_db), 
    embedding_id: int = 0
):
    """
    修改嵌入模型配置
    :param request: 包含更新参数的请求体
    :param session: 数据库会话
    :param embedding_id: 要修改的嵌入模型ID
    :return: 修改结果
    """
    update_data = request.dict(exclude_unset=True)
    embedding_manager.update_embedding(session, embedding_id, **update_data)
    return {"code": 200, "msg": "success"}


@router.delete("/embeddings")
def del_embedding(
    session: SyncSessionLocal = Depends(get_sync_db), 
    embedding_id: str = ""
):
    """
    删除嵌入模型配置
    :param session: 数据库会话
    :param embedding_id: 要删除的嵌入模型ID
    :return: 删除结果
    """
    embedding_manager.delete_embedding(session, embedding_id)
    return {"code": 200, "msg": "success"}


@router.get("/embeddings/list")
def get_embedding_list(session: SyncSessionLocal = Depends(get_sync_db)):
    """
    获取嵌入模型列表
    :param session: 数据库会话
    :return: 嵌入模型列表
    """
    return embedding_manager.get_embeddings(session)