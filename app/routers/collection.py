# -*- coding: UTF-8 -*-
"""
知识库管理

Author: worship-dog
Email: worship76@foxmail.com>
"""

from fastapi import APIRouter, Depends

from app.utils.database import get_sync_db, SyncSessionLocal
from app.services.collection import collection_manager


router = APIRouter(
    tags=["collection"],
    dependencies=[Depends(get_sync_db)]
)


@router.post("/collection")
def create_collection(session: SyncSessionLocal = Depends(get_sync_db), **kwargs):
    """
    创建知识库
    :param session: 数据库会话
    :param kwargs: 创建知识库所需的参数
    :return: 创建成功的知识库信息
    """
    collection_manager.add_collection(session, **kwargs)
    return {"code": 200, "msg": "success"}


@router.put("/collection")
def edit_collection(session: SyncSessionLocal = Depends(get_sync_db), collection_id: str="", **kwargs):
    """
    修改知识库信息
    :param session: 数据库会话
    :param collection_id: 要修改的知识库 ID
    :param kwargs: 要修改的知识库参数
    :return: 修改后的知识库信息
    """
    collection_manager.update_collection(session, collection_id, **kwargs)
    return {"code": 200, "msg": "success"}


@router.delete("/collection")
def del_collection(session: SyncSessionLocal = Depends(get_sync_db), collection_id: str=""):
    """
    删除知识库
    :param session: 数据库会话
    :param collection_id: 要删除的知识库 ID
    :return: 删除结果
    """
    collection_manager.delete_collection(session, collection_id)
    return {"code": 200, "msg": "success"}


@router.get("/collection/list")
def get_collection_list(session: SyncSessionLocal = Depends(get_sync_db)):
    """
    获取知识库列表
    :param session: 数据库会话
    :return: 知识库列表
    """
    return collection_manager.get_collections(session)
