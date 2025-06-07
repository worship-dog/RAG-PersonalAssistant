from langchain_ollama import OllamaEmbeddings
from langchain_postgres import PGVector

from app.utils.database import ASYNC_SQLALCHEMY_DATABASE_URL, SQLALCHEMY_DATABASE_URL


class VectorManager:
    def __init__(self):
        self.vector_dict = {}

    def get_vector(self, collection_name: str, embeddings: OllamaEmbeddings, async_mode:bool=False) -> PGVector:
        vector_key = f"{collection_name}_{embeddings.model}_{str(async_mode)}"
        vector_store = self.vector_dict.get(vector_key)
        if vector_store is None:
            vector_store = PGVector(
                connection=ASYNC_SQLALCHEMY_DATABASE_URL if async_mode else SQLALCHEMY_DATABASE_URL,
                collection_name=collection_name,
                embeddings=embeddings,
                create_extension=False,
                async_mode=async_mode
            )
            self.vector_dict[vector_key] = vector_store
        return vector_store


vector_manager = VectorManager()

