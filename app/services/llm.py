# -*- coding: UTF-8 -*-
"""
大语言模型管理

Author: worship-dog
Email: worship76@foxmail.com>
"""

from app.models import LLM
from app.utils.database import SyncSessionLocal


class LLMManager:
    def get_llms(self, session: SyncSessionLocal):
        """
        查询所有LLM模型

        :return: 包含模型信息的字典列表
        """
        llm_list = session.query(
            LLM.id,
            LLM.source,
            LLM.name,
            LLM.base_url,
            LLM.api_key
        ).all()

        rows = [{
            "llm_id": llm.id,
            "source": llm.source,
            "name": llm.name,
            "base_url": llm.base_url,
            "api_key": llm.api_key
        } for llm in llm_list]
        return rows

    def add_llm(self, session: SyncSessionLocal, source: str, name: str, base_url: str, api_key: str):
        """
        新增LLM模型记录到数据库

        :param source: 模型来源(ollama/openai/other)
        :param name: 模型名称
        :param base_url: 服务地址
        :param api_key: API密钥
        :return:
        """
        llm = LLM(
            source=source,
            name=name,
            base_url=base_url,
            api_key=api_key
        )
        session.add(llm)
        session.commit()

    def update_llm(self, session: SyncSessionLocal, llm_id: int, **kwargs):
        """
        更新LLM模型记录

        :param llm_id: 模型ID
        :param kwargs: 可更新字段(source, name, base_url, api_key)
        :return:
        """
        llm = session.query(LLM).filter(LLM.id == llm_id).first()
        if llm:
            for key, value in kwargs.items():
                if hasattr(llm, key):
                    setattr(llm, key, value)
            session.commit()

    def delete_llm(self, session: SyncSessionLocal, llm_id: int):
        """
        根据ID删除LLM模型记录

        :param llm_id: 要删除的模型ID
        :return: 如果删除成功返回True，未找到则返回False
        """
        llm = session.query(LLM).filter(LLM.id == llm_id).first()
        if llm:
            session.delete(llm)
            session.commit()
            return True
        return False


llm_manager = LLMManager()