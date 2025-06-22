# -*- coding: UTF-8 -*-
"""
提示词模板服务

Author: worship-dog
Email: worship76@foxmail.com>
"""

from app.models.prompt_template import PromptTemplate
from app.utils.database import Session


class PromptTemplateManager:
    def get_templates(self, session: Session):
        """
        获取所有提示词模板
        :param session: 数据库会话
        :return: 提示词模板列表
        """
        templates = session.query(
            PromptTemplate.id,
            PromptTemplate.name,
            PromptTemplate.content
        ).all()

        return [{
            "id": template.id,
            "name": template.name,
            "content": template.content
        } for template in templates]

    def add_template(self, session: Session, name: str, content: str):
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

    def update_template(self, session: Session, prompt_template_id: int, **kwargs):
        """
        更新提示词模板
        :param session: 数据库会话
        :param prompt_template_id: 模板ID
        :param kwargs: 可更新字段(name, content)
        :return:
        """
        template = session.query(PromptTemplate).filter(PromptTemplate.id == prompt_template_id).first()
        if template:
            for key, value in kwargs.items():
                if hasattr(template, key):
                    setattr(template, key, value)
            session.commit()

    def delete_template(self, session: Session, template_id: int):
        """
        删除提示词模板
        :param session: 数据库会话
        :param template_id: 要删除的模板ID
        :return: 如果删除成功返回True，未找到则返回False
        """
        template = session.query(PromptTemplate).filter(PromptTemplate.id == template_id).first()
        if template:
            session.delete(template)
            session.commit()
            return True
        return False


prompt_template_manager = PromptTemplateManager()