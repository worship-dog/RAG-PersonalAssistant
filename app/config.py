from sys import modules

from app.utils import get_config_obj


embeddings_config = {
    "source": (str, "ollama"),
    "model": (str, "bge-m3"),
    "base_url": (str, "http://localhost:11434")
}

def get_config(config_name: str):
    current_module = modules[__name__]  # 获取当前模块对象
    if hasattr(current_module, config_name):
        config_dict = getattr(current_module, config_name)  # 根据变量名获取config字典
        config_obj = get_config_obj(config_dict)  # 根据config字典动态创建config对象
        return config_obj
