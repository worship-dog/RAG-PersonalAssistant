# -*- coding: UTF-8 -*-
"""
知识库文件管理

Author: worship-dog
Email: worship76@foxmail.com>
"""
from datetime import datetime

from fastapi import APIRouter, Depends, Form, File, UploadFile, Query

from app.models import LangchainPGEmbedding
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
    embeddings_id: str = Form(...),
    tags: str = Form(None)
):
    embeddings = embeddings_manager.get_embeddings_by_id(session, embeddings_id)
    if not embeddings:
        return {"code": 404, "msg": "嵌入模型不存在"}
    vector_store = vector_manager.get_vector("默认知识库", embeddings.init())
    # TODO: 解析不同文件格式
    vector_store.add_texts([file.file.read()], [{
        "filename": file.filename,
        "modify_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "tag_list": tags.split(",") if tags else [],
        "index": 0
    }])
    return {"code": 200, "msg": "success"}


@router.delete("/knowledge")
def del_knowledge(
    session: Session = Depends(get_sync_db),
    filename: str = Query(...),
):
    file = session.query(LangchainPGEmbedding).filter(
        LangchainPGEmbedding.cmetadata.op("->>")("filename") == filename).first()
    session.delete(file)
    session.commit()
    return {"code": 200, "msg": "success"}


@router.get("/knowledge/list")
def get_knowledge_list(
    session: Session = Depends(get_sync_db)
):
    rows = []
    file_list = session.query(LangchainPGEmbedding.cmetadata).filter(
        LangchainPGEmbedding.cmetadata.op("->>")("index") == "0").all()
    for file in file_list:
        rows.append(file.cmetadata)
    return {"code": 200, "msg": "success", "data": rows}
