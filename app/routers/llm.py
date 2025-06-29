# -*- coding: UTF-8 -*-
"""
大语言模型管理

Author: worship-dog
Email: worship76@foxmail.com>
"""

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.services import llm_manager
from app.utils.database import get_sync_db, Session


router = APIRouter(
    tags=["llm"],
    dependencies=[Depends(get_sync_db)]
)


class LLMCreateRequest(BaseModel):
    source: str
    name: str
    base_url: str
    api_key: str = None


class LLMDeleteRequest(BaseModel):
    llm_id: str


class LLMUpdateRequest(LLMCreateRequest, LLMDeleteRequest):
    pass


@router.post("/llm")
def create_llm(
    request: LLMCreateRequest,
    session: Session = Depends(get_sync_db)
):
    """ 创建大语言模型配置 """
    create_data = request.model_dump(exclude_unset=True)
    llm_manager.add_llm(session, **create_data)
    return {"code": 200, "msg": "success"}

@router.put("/llm")
def edit_llm(
    request: LLMUpdateRequest,
    session: Session = Depends(get_sync_db)
):
    """
    修改大语言模型配置
    :param request: 包含更新参数的请求体
    :param session: 数据库会话
    :return: 修改结果
    """
    update_data = request.model_dump(exclude_unset=True)
    llm_manager.update_llm(session, **update_data)
    return {"code": 200, "msg": "success"}

@router.delete("/llm")
def del_llm(
    request: LLMDeleteRequest,
    session: Session = Depends(get_sync_db)
):
    """
    删除大语言模型配置
    :param request: 包含删除参数的请求体
    :param session: 数据库会话
    :return: 删除结果
    """
    llm_manager.delete_llm(session, request.llm_id)
    return {"code": 200, "msg": "success"}


@router.get("/llm/list")
def get_llm_list(session: Session = Depends(get_sync_db)):
    """
    获取大语言模型列表
    :param session: 数据库会话
    :return: 大语言模型列表
    """
    llm_list = llm_manager.get_llm_list(session)
    return {"code": 200, "message": "success", "data": llm_list}