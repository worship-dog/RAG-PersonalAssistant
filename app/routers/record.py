# -*- coding: UTF-8 -*-
"""
记录管理

Author: worship-dog
Email: worship76@foxmail.com>
"""

from fastapi import APIRouter, Depends

from app.utils.database import get_sync_db


router = APIRouter(
    tags=["record"],
    dependencies=[Depends(get_sync_db)]
)


@router.post("/record")
def create_record():
    pass


@router.get("/record")
def get_record():
    pass


@router.put("/record")
def edit_record():
    pass


@router.delete("/record")
def del_record():
    pass


@router.get("/record/list")
def get_record_list():
    pass
