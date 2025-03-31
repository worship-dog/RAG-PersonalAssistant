from langchain_ollama import OllamaEmbeddings

from app.config import get_config


embeddings_source_dict = {"ollama": OllamaEmbeddings, "openai": OllamaEmbeddings}

embeddings_config = get_config("embeddings_config")
embeddings_class = embeddings_source_dict[embeddings_config.source]

embeddings = embeddings_class(model=embeddings_config.model, base_url=embeddings_config.base_url)
