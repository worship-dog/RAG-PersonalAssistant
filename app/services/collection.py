# -*- coding: UTF-8 -*-
"""
知识库管理

Author: worship-dog
Email: worship76@foxmail.com>
"""

import uuid

from app.models import Knowledge, LangchainPGCollection, LangchainPGEmbedding
from app.utils.database import Session


class CollectionManager:
    @staticmethod
    def get_collection_by_id(session: Session, collection_id: str):
        """
        根据 ID 查询知识库

        :param session: 数据库会话
        :param collection_id: 要查询的知识库 ID
        :return: 匹配的 LangchainPGCollection 对象，如果没有匹配项则返回 None
        """
        return session.query(LangchainPGCollection).filter_by(uuid=collection_id).first()

    @staticmethod
    def get_collections(session: Session):
        """
        查询知识库

        :param session: 数据库会话
        :return: 包含知识库信息的字典列表
        """
        collections = session.query(
            LangchainPGCollection.uuid, LangchainPGCollection.name, LangchainPGCollection.cmetadata
        ).all()

        rows = [{
            "collection_id": collection.uuid,
            "name": collection.name,
            "display": collection.cmetadata.get("display") if collection.cmetadata else ""
        } for collection in collections]
        return rows

    @staticmethod
    def add_collection(session: Session, name: str, display: str):
        """
        新增知识库记录到数据库

        :param session: 数据库会话
        :param name: 知识库名称
        :param display: 知识库描述
        :return:
        """
        collection = LangchainPGCollection(name=name, cmetadata={"display": display})
        collection.uuid = str(uuid.uuid4())
        session.add(collection)
        session.commit()

    @staticmethod
    def update_collection(session: Session, collection_id: str, name: str = None, display: str = None):
        """
        根据 ID 修改知识库记录

        :param session: 数据库会话
        :param collection_id: 要修改的知识库 ID
        :param name: 新的知识库名称，可选
        :param display: 新的知识库元数据，可选
        :return:
        """
        collection = session.query(LangchainPGCollection).filter_by(uuid=collection_id).first()
        if collection:
            if name:
                collection.name = name
            if display:
                collection.cmetadata = {"display": display}
            session.commit()

    @staticmethod
    def delete_collection(session: Session, collection_id: str):
        """
        根据 ID 删除知识库记录

        :param session: 数据库会话
        :param collection_id: 要删除的知识库 ID
        :return: 如果删除成功返回 True，未找到则返回 False
        """
        collection = session.query(LangchainPGCollection).filter_by(uuid=collection_id).first()
        if collection:
            # 删除相关的知识嵌入
            for embedding in session.query(LangchainPGEmbedding).filter_by(collection_id=collection_id).all():
                session.delete(embedding)
            # 删除相关的知识
            for knowledge in session.query(Knowledge).filter_by(collection_id=collection_id).all():
                session.delete(knowledge)

            session.delete(collection)
            session.commit()


collection_manager = CollectionManager()
