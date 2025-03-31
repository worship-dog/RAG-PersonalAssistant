from pydantic import create_model

def get_config_obj(config_dict: dict):
    config_class = create_model("config", **config_dict)
    return config_class()
