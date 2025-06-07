# -*- coding: UTF-8 -*-
"""
知识库文件管理

Author: worship-dog
Email: worship76@foxmail.com>
"""
import os

from fastapi import APIRouter, Depends, Form, File, UploadFile

from app.services.collection import collection_manager
from app.services.embeddings import embeddings_manager
from app.utils.database import get_sync_db, Session
from app.utils.vector import vector_manager


router = APIRouter(
    tags=["knowledge"],
    dependencies=[Depends(get_sync_db)]
)


@router.post("/knowledge")
async def create_knowledge(
    session: Session = Depends(get_sync_db),
    file: UploadFile = File(...),
    collection_id: str = Form(...),
    embeddings_id: str = Form(...)
):
    collection = collection_manager.get_collection_by_id(session, collection_id)
    if not collection:
        return {"code": 404, "msg": "知识库不存在"}
    embeddings = embeddings_manager.get_embeddings_by_id(session, embeddings_id)
    if not embeddings:
        return {"code": 404, "msg": "嵌入模型不存在"}
    vector_store = vector_manager.get_vector(collection.name, embeddings.init())
    # TODO: 解析不同文件格式
    vector_store.add_texts([file.file.read()], [{"filename": file.filename}])
    return {"code": 200, "msg": "上传成功"}

@router.get("/knowledge")
def get_knowledge():
    pass


@router.put("/knowledge")
def edit_knowledge():
    pass


@router.delete("/knowledge")
def del_knowledge(file_name: str, collection_id: str = None):
    """
    删除知识库文件
    :param file_name: 要删除的文件名
    :param collection_id: 关联的知识库
    :return: 删除结果
    """
    save_dir = f"static/knowledge/{collection_id}"
    file_path = os.path.join(save_dir, file_name)
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            return {"code": 200, "msg": f"文件 {file_name} 删除成功"}
        else:
            return {"code": 404, "msg": f"文件 {file_name} 不存在"}
    except Exception as e:
        return {"code": 500, "msg": f"文件删除失败: {str(e)}"}


@router.get("/knowledge/list")
def get_knowledge_list(collection_id: str = None):
    """
    获取知识库文件列表
    :param collection_id: 关联的知识库 ID
    :return: 文件列表
    """
    save_dir = f"static/knowledge/{collection_id}"
    try:
        if os.path.exists(save_dir):
            file_list = os.listdir(save_dir)
            return {"code": 200, "msg": "获取文件列表成功", "data": file_list}
        else:
            return {"code": 404, "msg": "知识库目录不存在", "data": []}
    except Exception as e:
        return {"code": 500, "msg": f"获取文件列表失败: {str(e)}", "data": []}
