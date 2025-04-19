# -*- coding: UTF-8 -*-
"""
大语言模型管理

Author: worship-dog
Email: worship76@foxmail.com>
"""

from app.models import LLM
from app.utils.database import SyncSessionLocal


class LLMManager:
    def get_models(self, session: SyncSessionLocal):
        """
        查询所有LLM模型

        :return: 包含模型信息的字典列表
        """
        models = session.query(
            LLM.id,
            LLM.source,
            LLM.name,
            LLM.base_url,
            LLM.api_key
        ).all()

        rows = [{
            "id": model.id,
            "source": model.source,
            "name": model.name,
            "base_url": model.base_url,
            "api_key": model.api_key
        } for model in models]
        return rows

    def add_model(self, session: SyncSessionLocal, source: str, name: str, base_url: str, api_key: str):
        """
        新增LLM模型记录到数据库

        :param source: 模型来源(ollama/openai/other)
        :param name: 模型名称
        :param base_url: 服务地址
        :param api_key: API密钥
        :return:
        """
        model = LLM(
            source=source,
            name=name,
            base_url=base_url,
            api_key=api_key
        )
        session.add(model)
        session.commit()

    def update_model(self, session: SyncSessionLocal, model_id: int, **kwargs):
        """
        更新LLM模型记录

        :param model_id: 模型ID
        :param kwargs: 可更新字段(source, name, base_url, api_key)
        :return:
        """
        model = session.query(LLM).filter(LLM.id == model_id).first()
        if model:
            for key, value in kwargs.items():
                if hasattr(model, key):
                    setattr(model, key, value)
            session.commit()

    def delete_model(self, session: SyncSessionLocal, model_id: int):
        """
        根据ID删除LLM模型记录

        :param model_id: 要删除的模型ID
        :return: 如果删除成功返回True，未找到则返回False
        """
        model = session.query(LLM).filter(LLM.id == model_id).first()
        if model:
            session.delete(model)
            session.commit()
            return True
        return False


llm_manager = LLMManager()