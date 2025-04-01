from sys import modules

from app.utils.dict2obj import get_config_obj


llm_config = {
    "source": (str, "ollama"),
    "model": (str, "deepseek-r1:8b"),
    "base_url": (str, "http://localhost:11434")
}
embeddings_config = {
    "source": (str, "ollama"),
    "model": (str, "bge-m3"),
    "base_url": (str, "http://localhost:11434")
}

db_config = {
    "db_host": (str, "localhost"),
    "db_port": (str, "5432"),
    "db_name": (str, "db_personal_assistant"),
    "username": (str, "admin"),
    "password": (str, "admin123"),
    "pool_size": (int, 10),
    "max_overflow": (int, 20)
}

def get_config(config_name: str):
    current_module = modules[__name__]  # 获取当前模块对象
    if hasattr(current_module, config_name):
        config_dict = getattr(current_module, config_name)  # 根据变量名获取config字典
        config_obj = get_config_obj(config_dict)  # 根据config字典动态创建config对象
        return config_obj
