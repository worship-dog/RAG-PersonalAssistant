# -*- coding: UTF-8 -*-
"""
项目配置

Author: worship-dog
Email: worship76@foxmail.com>
"""

from pydantic import create_model
from sys import modules


# 数据库配置
db_config = {
    "db_host": (str, "localhost"),
    "db_port": (str, "5432"),
    "db_name": (str, "db_personal_assistant"),
    "username": (str, "admin"),
    "password": (str, "admin123"),
    "pool_size": (int, 10),
    "max_overflow": (int, 20)
}

# redis配置
redis_config = {
    "host": (str, "localhost"),
    "port": (int, 6379),
    "db": (int, 0),
}

# 历史聊天记录配置
HISTORY_MAX_LENGTH = 40  # 历史聊天记录最大长度
HISTORY_EXPIRE_TIME = 60 * 60 * 24 * 7  # 历史聊天记录在Redis中的过期时间, 单位秒, 7天

# 知识库配置
MIN_SIMILARITY = 0.7  # 知识库检索的最小相似度

# 路由配置
ROUTER_PREFIX = "/api"  # 路由前缀

# 用户配置(未使用)
USERNAME = ""  # 用户名
AVATAR = ""  # 用户头像


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
