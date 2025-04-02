# -*- coding: UTF-8 -*-
"""
知识库管理

Author: worship-dog
Email: worship76@foxmail.com>
"""

from fastapi import APIRouter, Depends

from app.utils.database import get_db


router = APIRouter(
    tags=["collection"],
    dependencies=[Depends(get_db)]
)


@router.post("/collection")
def create_collection():
    pass


@router.get("/collection")
def get_collection():
    pass


@router.put("/collection")
def edit_collection():
    pass


@router.delete("/collection")
def del_collection():
    pass


@router.get("/collection/list")
def get_collection_list():
    pass
