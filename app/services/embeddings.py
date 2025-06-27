# -*- coding: UTF-8 -*-
"""
嵌入模型管理

Author: worship-dog
Email: worship76@foxmail.com>
"""

from sqlalchemy import desc
from app.models.embeddings import Embeddings
from app.utils.database import Session


class EmbeddingsManager:

    @staticmethod
    def get_default_embeddings(session: Session):
        """
        获取默认的嵌入模型

        :param session: 数据库会话
        :return: 嵌入模型信息
        """
        return session.query(Embeddings).filter_by(default=True).first()

    @staticmethod
    def get_embeddings_by_id(session: Session, embeddings_id: str):
        """
        根据ID查询嵌入模型

        :param session: 数据库会话
        :param embeddings_id: 嵌入模型ID
        :return: 嵌入模型信息
        """
        return session.query(Embeddings).filter_by(id=embeddings_id).first()

    @staticmethod
    def get_embeddings_by_name(session: Session, embeddings_name: str):
        """
        根据ID查询嵌入模型

        :param session: 数据库会话
        :param embeddings_name: 嵌入模型名
        :return: 嵌入模型信息
        """
        return session.query(Embeddings).filter_by(name=embeddings_name).first()

    @staticmethod
    def get_embeddings_list(session: Session):
        """
        查询所有嵌入模型

        :param session: 数据库会话
        :return: 包含嵌入模型信息的字典列表
        """
        embeddings_list = session.query(
            Embeddings.id,
            Embeddings.source,
            Embeddings.name,
            Embeddings.base_url,
            Embeddings.default
        ).order_by(
            desc(Embeddings.default), 
            desc(Embeddings.update_time), 
            Embeddings.name
        ).all()

        rows = [{
            "embeddings_id": embeddings.id,
            "source": embeddings.source,
            "name": embeddings.name,
            "base_url": embeddings.base_url,
            "default": embeddings.default
        } for embeddings in embeddings_list]
        return rows

    @staticmethod
    def add_embeddings(session: Session, source: str, name: str, base_url: str, default: bool):
        """
        新增嵌入模型到数据库

        :param session: 数据库会话
        :param source: 模型来源(ollama/openai/other)
        :param name: 模型名称
        :param base_url: 服务地址
        :param default: 是否为默认模型
        :return:
        """
        if default:
            # 检查是否存在其他默认嵌入模型
            if default_embeddings := EmbeddingsManager.get_default_embeddings(session):
                # 如果存在，将其设为非默认
                default_embeddings.default = False
        
        embeddings = Embeddings(
            source=source,
            name=name,
            base_url=base_url,
            default=default
        )
        session.add(embeddings)
        session.commit()

    @staticmethod
    def update_embeddings(session: Session, embeddings_id: int, **kwargs):
        """
        更新嵌入模型

        :param session: 数据库会话
        :param embeddings_id: 嵌入模型ID
        :param kwargs: 可更新字段(source, name, base_url)
        :return:
        """
        if kwargs.get("default"):
            # 检查是否存在默认嵌入模型
            if default_embeddings := EmbeddingsManager.get_default_embeddings(session):
                # 如果存在且并非当前模型，将其设为非默认
                if default_embeddings.id != embeddings_id:
                    default_embeddings.default = False

        embeddings = session.query(Embeddings).filter_by(id=embeddings_id).first()
        if embeddings:
            for key, value in kwargs.items():
                if hasattr(embeddings, key):
                    setattr(embeddings, key, value)
            session.commit()

    @staticmethod
    def delete_embeddings(session: Session, embeddings_id: int):
        """
        根据ID删除嵌入模型

        :param session: 数据库会话
        :param embeddings_id: 要删除的嵌入模型ID
        :return: 如果删除成功返回True，未找到则返回False
        """
        embeddings = session.query(Embeddings).filter_by(id=embeddings_id).first()
        if embeddings:
            session.delete(embeddings)
            session.commit()
            return True
        return False


embeddings_manager = EmbeddingsManager()