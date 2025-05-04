# -*- coding: UTF-8 -*-
"""
知识库管理

Author: worship-dog
Email: worship76@foxmail.com>
"""

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.services import collection_manager
from app.utils.database import get_sync_db, Session


router = APIRouter(
    tags=["conversation"],
    dependencies=[Depends(get_sync_db)]
)


class CollectionCreateRequest(BaseModel):
    name: str = None
    display: str = None


class CollectionDeleteRequest(BaseModel):
    collection_id: str


class CollectionUpdateRequest(CollectionCreateRequest, CollectionDeleteRequest):
    pass


@router.post("/collection")
def create_collection(
    request: CollectionCreateRequest,
    session: Session = Depends(get_sync_db)
):
    """
    创建知识库
    :param request: 包含创建参数的请求体
    :param session: 数据库会话
    :return: 创建成功的知识库信息
    """
    create_data = request.model_dump(exclude_unset=True)
    collection_manager.add_collection(session, **create_data)
    return {"code": 200, "msg": "success"}

@router.put("/collection")
def edit_collection(
    request: CollectionUpdateRequest,
    session: Session = Depends(get_sync_db)
):
    """
    修改知识库信息
    :param request: 包含更新参数的请求体
    :param session: 数据库会话
    :return: 修改后的知识库信息
    """
    update_data = request.model_dump(exclude_unset=True)
    collection_manager.update_collection(session, **update_data)
    return {"code": 200, "msg": "success"}

@router.delete("/collection")
def del_collection(
    request: CollectionDeleteRequest,
    session: Session = Depends(get_sync_db)
):
    """
    删除知识库
    :param request: 包含删除参数的请求体
    :param session: 数据库会话
    :return: 删除结果
    """
    collection_manager.delete_collection(session, request.collection_id)
    return {"code": 200, "msg": "success"}


@router.get("/collection/list")
def get_collection_list(session: Session = Depends(get_sync_db)):
    """
    获取知识库列表
    :param session: 数据库会话
    :return: 知识库列表
    """
    collections = collection_manager.get_collections(session)
    return {"code": 200, "msg": "success", "data": collections}
