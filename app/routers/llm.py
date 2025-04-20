# -*- coding: UTF-8 -*-
"""
大语言模型管理

Author: worship-dog
Email: worship76@foxmail.com>
"""

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.utils.database import get_sync_db, SyncSessionLocal
from app.services.llm import llm_manager


router = APIRouter(
    tags=["llm"],
    dependencies=[Depends(get_sync_db)]
)


class LLMRequest(BaseModel):
    source: str
    name: str
    base_url: str
    api_key: str = None


@router.post("/llm")
def create_llm(
    request: LLMRequest,
    session: SyncSessionLocal = Depends(get_sync_db)
):
    """
    创建大语言模型配置
    :param request: 包含创建参数的请求体
    :param session: 数据库会话
    :return: 创建结果
    """
    llm_manager.add_model(session, **request.dict())
    return {"code": 200, "msg": "success"}

@router.put("/llm")
def edit_llm(
    request: LLMRequest,
    session: SyncSessionLocal = Depends(get_sync_db), 
    model_id: int = 0
):
    """
    修改大语言模型配置
    :param request: 包含更新参数的请求体
    :param session: 数据库会话
    :param model_id: 要修改的大语言模型ID
    :return: 修改结果
    """
    update_data = request.dict(exclude_unset=True)
    llm_manager.update_model(session, model_id, **update_data)
    return {"code": 200, "msg": "success"}

@router.delete("/llm")
def del_llm(
    session: SyncSessionLocal = Depends(get_sync_db), 
    model_id: str = ""
):
    """
    删除大语言模型配置
    :param session: 数据库会话
    :param model_id: 要删除的大语言模型ID
    :return: 删除结果
    """
    llm_manager.delete_model(session, model_id)
    return {"code": 200, "msg": "success"}


@router.get("/llm/list")
def get_llm_list(session: SyncSessionLocal = Depends(get_sync_db)):
    """
    获取大语言模型列表
    :param session: 数据库会话
    :return: 大语言模型列表
    """
    return llm_manager.get_models(session)