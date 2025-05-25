# -*- coding: UTF-8 -*-
"""
项目配置

Author: worship-dog
Email: worship76@foxmail.com>
"""

from pydantic import create_model
from sys import modules


db_config = {
    "db_host": (str, "localhost"),
    "db_port": (str, "5432"),
    "db_name": (str, "db_personal_assistant"),
    "username": (str, "admin"),
    "password": (str, "admin123"),
    "pool_size": (int, 10),
    "max_overflow": (int, 20)
}

user_name = ""
avatar = ""


# 字典转对象
def dict2obj(config_dict: dict):
    config_class = create_model("config", **config_dict)  # 根据config字典动态创建类
    return config_class()


# 根据变量名获取config对象
def get_config(config_name: str):
    current_module = modules[__name__]  # 获取当前模块对象
    if hasattr(current_module, config_name):
        config_dict = getattr(current_module, config_name)  # 根据变量名获取config字典
        config_obj = dict2obj(config_dict)  # 根据config字典动态创建config对象
        return config_obj
    else:
        raise AttributeError(f"{config_name} is not exist")
