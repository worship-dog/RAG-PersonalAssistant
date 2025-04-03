# -*- coding: UTF-8 -*-
"""
知识库文件管理

Author: worship-dog
Email: worship76@foxmail.com>
"""

from fastapi import APIRouter, Depends

from app.utils.database import get_sync_db


router = APIRouter(
    tags=["knowledge"],
    dependencies=[Depends(get_sync_db)]
)


@router.post("/knowledge")
def create_knowledge():
    pass


@router.get("/knowledge")
def get_knowledge():
    pass


@router.put("/knowledge")
def edit_knowledge():
    pass


@router.delete("/knowledge")
def del_knowledge():
    pass


@router.get("/knowledge/list")
def get_knowledge_list():
    pass
