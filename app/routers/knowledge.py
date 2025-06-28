# -*- coding: UTF-8 -*-
"""
知识库文件管理

Author: worship-dog
Email: worship76@foxmail.com>
"""
from datetime import datetime

from fastapi import APIRouter, Depends, Form, File, Query, UploadFile, HTTPException

from app.models import LangchainPGEmbedding
from app.services.embeddings import embeddings_manager
from app.utils.database import get_sync_db, Session
from app.utils.vector import vector_manager


router = APIRouter(
    tags=["knowledge"],
    dependencies=[Depends(get_sync_db)]
)


def add_knowledge(
    session: Session,
    file: UploadFile,
    embeddings_id: str,
    tags: str = None
):
    embeddings = embeddings_manager.get_embeddings_by_id(session, embeddings_id)
    if not embeddings:
        return {"code": 404, "msg": "嵌入模型不存在"}
    
    vector_store = vector_manager.get_vector(embeddings.init())

    # 验证文件名是否重复
    if vector_store.similarity_search(file.filename, filter={"filename": file.filename}):
        raise HTTPException(status_code=400, detail="文件名重复")

    # TODO: 解析不同文件格式
    vector_store.add_texts([file.file.read()], [{
        "filename": file.filename,
        "modify_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "tag_list": list(set(tags.split(","))) if tags else [],
        "index": 0
    }])
    return {"code": 200, "msg": "success"}


@router.post("/knowledge")
async def create_knowledge(
    session: Session = Depends(get_sync_db),
    file: UploadFile = File(...),
    embeddings_id: str = Form(...),
    tags: str = Form(None)
):
    return add_knowledge(session, file, embeddings_id, tags)


@router.put("/knowledge")
def edit_knowledge(
    session: Session = Depends(get_sync_db),
    filename: str = Form(...),
    file: UploadFile = File(None),
    embeddings_id: str = Form(None),
    tags: str = Form(None)
):
    knowledge_list = session.query(LangchainPGEmbedding).filter(
        LangchainPGEmbedding.cmetadata.op("->>")("filename") == filename).all()
    if file.size != 0:
        for knowledge in knowledge_list:
            session.delete(knowledge)
        result = add_knowledge(session, file, embeddings_id, tags)
        session.commit()
        return result
    
    modify_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    for knowledge in knowledge_list:
        knowledge.cmetadata = {
            "filename": filename,
            "modify_time": modify_time,
            "tag_list": list(set(tags.split(","))) if tags else [],
            "index": knowledge.cmetadata.get("index")
        }
    session.commit()
        
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
        LangchainPGEmbedding.cmetadata.op("->>")("index") == "0").order_by(
            LangchainPGEmbedding.cmetadata.op("->>")("modify_time").desc()
        ).all()
    for file in file_list:
        rows.append(file.cmetadata)
    return {"code": 200, "msg": "success", "data": rows}
