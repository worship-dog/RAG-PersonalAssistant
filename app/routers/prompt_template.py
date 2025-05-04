# -*- coding: UTF-8 -*-
"""
提示词模板路由

Author: worship-dog
Email: worship76@foxmail.com>
"""

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.services import prompt_template_manager
from app.utils.database import get_sync_db, Session


router = APIRouter(
    tags=["prompt_template"],
    dependencies=[Depends(get_sync_db)]
)


class PromptTemplateCreateRequest(BaseModel):
    name: str
    content: str


class PromptTemplateDeleteRequest(BaseModel):
    prompt_template_id: str


class PromptTemplateUpdateRequest(PromptTemplateCreateRequest, PromptTemplateDeleteRequest):
    pass


@router.post("/prompt_template")
def create_template(
    request: PromptTemplateCreateRequest,
    session: Session = Depends(get_sync_db)
):
    """
    创建提示词模板
    :param request: 包含创建参数的请求体
    :param session: 数据库会话
    :return: 创建结果
    """
    create_data = request.model_dump(exclude_unset=True)
    prompt_template_manager.add_template(session, **create_data)
    return {"code": 200, "msg": "success"}


@router.put("/prompt_template")
def update_template(
    request: PromptTemplateUpdateRequest,
    session: Session = Depends(get_sync_db)
):
    """
    更新提示词模板
    :param request: 包含更新参数的请求体
    :param session: 数据库会话
    :return: 更新结果
    """
    update_data = request.model_dump(exclude_unset=True)
    prompt_template_manager.update_template(session, **update_data)
    return {"code": 200, "msg": "success"}


@router.delete("/prompt_template")
def delete_template(
    request: PromptTemplateDeleteRequest,
    session: Session = Depends(get_sync_db)
):
    """
    删除提示词模板
    :param request: 包含删除参数的请求体
    :param session: 数据库会话
    :return: 删除结果
    """
    prompt_template_manager.delete_template(session, request.prompt_template_id)
    return {"code": 200, "msg": "success"}


@router.get("/prompt_template/list")
def get_template_list(session: Session = Depends(get_sync_db)):
    """
    获取提示词模板列表
    :param session: 数据库会话
    :return: 提示词模板列表
    """
    return prompt_template_manager.get_templates(session)