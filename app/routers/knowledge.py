# -*- coding: UTF-8 -*-
"""
知识库文件管理

Author: worship-dog
Email: worship76@foxmail.com>
"""
from datetime import datetime
import os
import tempfile

from fastapi import APIRouter, Depends, Form, File, Query, UploadFile, HTTPException
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.models import LangchainPGEmbedding
from app.services.embeddings import embeddings_manager
from app.utils.database import get_sync_db, Session
from app.utils.file_tools import read_file
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

    # 获取文件类型
    file_type = file.filename.split(".")[-1]
    
    # 创建临时文件并保存上传的文件内容
    with tempfile.NamedTemporaryFile(delete=False, suffix=f'.{file_type}') as temp_file:
        temp_file.write(file.file.read())
        temp_file_path = temp_file.name
    
    try:
        # 使用 read_file 函数读取文件内容
        file_content = read_file(temp_file_path, file_type)
        # 重置文件指针，以便后续操作可以重新读取文件内容
        file.file.seek(0)
    except ValueError as e:
        # 捕获并记录文件类型不支持的错误
        print(f"不支持的文件类型: {file_type}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        # 发生异常时记录错误并继续使用原始文件内容
        print(f"读取文件时出错: {str(e)}")
        file.file.seek(0)
        raise HTTPException(status_code=500, detail="文件读取错误")

    if not file_content:
        raise HTTPException(status_code=400, detail="未识别到有效内容")

    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    # 文本内容分块嵌入
    split_texts = splitter.split_text(file_content)
    vector_store.add_texts(split_texts, [{
        "filename": file.filename,
        "modify_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "tags": tags,
        "index": i + 1
    }for i in range(len(split_texts))])
    # 清理临时文件
    if os.path.exists(temp_file_path):
        os.unlink(temp_file_path)

    # # 新增知识对象
    # knowledge = Knowledge(
    #     name=file.filename,
    #     knowledge={"file_content": file_content},
    #     index=0
    # )
    # session.add(knowledge)
    # session.commit()
        
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
            "tags": tags,
            "index": knowledge.cmetadata.get("index")
        }
    session.commit()
        
    return {"code": 200, "msg": "success"}


@router.delete("/knowledge")
def del_knowledge(
    session: Session = Depends(get_sync_db),
    filename: str = Query(...),
):
    file_list = session.query(LangchainPGEmbedding).filter(
        LangchainPGEmbedding.cmetadata.op("->>")("filename") == filename).all()
    for file in file_list:
        session.delete(file)
    session.commit()
    return {"code": 200, "msg": "success"}


@router.get("/knowledge/list")
def get_knowledge_list(
    session: Session = Depends(get_sync_db)
):
    rows = []
    file_list = session.query(LangchainPGEmbedding.cmetadata).filter(
        LangchainPGEmbedding.cmetadata.op("->>")("index") == "1").order_by(
            LangchainPGEmbedding.cmetadata.op("->>")("modify_time").desc()
        ).all()
    for file in file_list:
        rows.append(file.cmetadata)
    return {"code": 200, "msg": "success", "data": rows}


@router.get("/knowledge/tags")
def get_knowledge_tags(
    session: Session = Depends(get_sync_db)
):
    tag_list = []
    file_list = session.query(LangchainPGEmbedding.cmetadata).group_by(LangchainPGEmbedding.cmetadata).all()
    for file in file_list:
        tags = file.cmetadata.get("tags")
        if not tags:
            continue
        tag_list.extend(tags.split(","))
    return {"code": 200, "msg": "success", "data": list(set(tag_list))}
