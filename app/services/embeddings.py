# -*- coding: UTF-8 -*-
"""
嵌入模型管理

Author: worship-dog
Email: worship76@foxmail.com>
"""

from app.models.embeddings import Embeddings
from app.utils.database import SyncSessionLocal


class EmbeddingsManager:
    def get_embeddings_list(self, session: SyncSessionLocal):
        """
        查询所有嵌入模型

        :return: 包含嵌入模型信息的字典列表
        """
        embeddings_list = session.query(
            Embeddings.id,
            Embeddings.source,
            Embeddings.name,
            Embeddings.base_url
        ).all()

        rows = [{
            "embeddings_id": embeddings.id,
            "source": embeddings.source,
            "name": embeddings.name,
            "base_url": embeddings.base_url
        } for embeddings in embeddings_list]
        return rows

    def add_embeddings(self, session: SyncSessionLocal, source: str, name: str, base_url: str):
        """
        新增嵌入模型到数据库

        :param source: 模型来源(ollama/openai/other)
        :param name: 模型名称
        :param base_url: 服务地址
        :return:
        """
        embeddings = Embeddings(
            source=source,
            name=name,
            base_url=base_url
        )
        session.add(embeddings)
        session.commit()

    def update_embeddings(self, session: SyncSessionLocal, embeddings_id: int, **kwargs):
        """
        更新嵌入模型

        :param embeddings_id: 嵌入模型ID
        :param kwargs: 可更新字段(source, name, base_url)
        :return:
        """
        embeddings = session.query(Embeddings).filter(Embeddings.id == embeddings_id).first()
        if embeddings:
            for key, value in kwargs.items():
                if hasattr(embeddings, key):
                    setattr(embeddings, key, value)
            session.commit()

    def delete_embeddings(self, session: SyncSessionLocal, embeddings_id: int):
        """
        根据ID删除嵌入模型

        :param embeddings_id: 要删除的嵌入模型ID
        :return: 如果删除成功返回True，未找到则返回False
        """
        embeddings = session.query(Embeddings).filter(Embeddings.id == embeddings_id).first()
        if embeddings:
            session.delete(embeddings)
            session.commit()
            return True
        return False


embeddings_manager = EmbeddingsManager()