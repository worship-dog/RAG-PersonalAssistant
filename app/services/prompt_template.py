# -*- coding: UTF-8 -*-
"""
提示词模板服务

Author: worship-dog
Email: worship76@foxmail.com>
"""
from sqlalchemy import desc

from app.models.prompt_template import PromptTemplate
from app.utils.database import Session


class PromptTemplateManager:
    @staticmethod
    def get_templates(session: Session):
        """
        获取所有提示词模板
        :param session: 数据库会话
        :return: 提示词模板列表
        """
        templates = session.query(
            PromptTemplate.id,
            PromptTemplate.name,
            PromptTemplate.content
        ).order_by(desc(PromptTemplate.update_time)).all()

        return [{
            "id": template.id,
            "name": template.name,
            "content": template.content
        } for template in templates]

    @staticmethod
    def add_template(session: Session, name: str, content: str):
        """
        添加提示词模板
        :param session: 数据库会话
        :param name: 模板名称
        :param content: 模板内容
        :return:
        """
        template = PromptTemplate(name=name, content=content)
        session.add(template)
        session.commit()

    @staticmethod
    def update_template(session: Session, prompt_template_id: int, **kwargs):
        """
        更新提示词模板
        :param session: 数据库会话
        :param prompt_template_id: 模板ID
        :param kwargs: 可更新字段(name, content)
        :return:
        """
        template = session.query(PromptTemplate).filter_by(id=prompt_template_id).first()
        if template:
            for key, value in kwargs.items():
                if hasattr(template, key):
                    setattr(template, key, value)
            session.commit()

    @staticmethod
    def delete_template(session: Session, template_id: int):
        """
        删除提示词模板
        :param session: 数据库会话
        :param template_id: 要删除的模板ID
        :return: 如果删除成功返回True，未找到则返回False
        """
        template = session.query(PromptTemplate).filter_by(id=template_id).first()
        if template:
            session.delete(template)
            session.commit()
            return True
        return False


prompt_template_manager = PromptTemplateManager()