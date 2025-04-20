# -*- coding: UTF-8 -*-
"""
知识库管理

Author: worship-dog
Email: worship76@foxmail.com>
"""

import json

from app.models import Knowledge, LangchainPGCollection, LangchainPGEmbedding
from app.utils.database import SyncSessionLocal


class CollectionManager:
    def get_collections(self, session: SyncSessionLocal):
        """
        查询知识库

        :return: 包含知识库信息的字典列表
        """
        collections = session.query(
            LangchainPGCollection.uuid, LangchainPGCollection.name, LangchainPGCollection.cmetadata
        ).all()

        rows = [{
            "collection_id": collection.uuid, "collection_name": collection.name, "collection_display": collection.cmetadata
        } for collection in collections]
        return rows

    def add_collection(self, session: SyncSessionLocal, name: str, display: str):
        """
        新增知识库记录到数据库

        :param name: 知识库名称
        :param display: 知识库描述
        :return:
        """
        collection = LangchainPGCollection(name=name, cmetadata={"display": display})
        session.add(collection)
        session.commit()

    def update_collection(self, session: SyncSessionLocal, collection_id: str, name: str = None, display: str = None):
        """
        根据 ID 修改知识库记录

        :param collection_id: 要修改的知识库 ID
        :param name: 新的知识库名称，可选
        :param display: 新的知识库元数据，可选
        :return:
        """
        collection = session.query(LangchainPGCollection).filter(LangchainPGCollection.uuid == collection_id).first()
        if collection:
            if name:
                collection.name = name
            if display:
                collection.cmetadata = {"display": display}
            session.commit()

    def delete_collection(self, session: SyncSessionLocal, collection_id: str):
        """
        根据 ID 删除知识库记录

        :param collection_id: 要删除的知识库 ID
        :return: 如果删除成功返回 True，未找到则返回 False
        """
        collection = session.query(LangchainPGCollection).filter(LangchainPGCollection.uuid == collection_id).first()
        if collection:
            # 删除相关的知识嵌入
            for embedding in session.query(LangchainPGEmbedding).filter(LangchainPGEmbedding.collection_id == collection_id).all():
                session.delete(embedding)
            # 删除相关的知识
            for knowledge in session.query(Knowledge).filter(Knowledge.collection_id == collection_id).all():
                session.delete(knowledge)

            session.delete(collection)
            session.commit()


collection_manager = CollectionManager()
