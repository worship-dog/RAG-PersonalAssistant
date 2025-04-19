from langchain_ollama import OllamaEmbeddings
from langchain_postgres import PGVector

from app.utils.database import SQLALCHEMY_DATABASE_URL


class Vector:
    def __init__(self):
        self.vector_dict = {}

    def __create_vector(self, collection_name: str, embeddings: OllamaEmbeddings) -> PGVector:
        vector_key = f"{collection_name}_{embeddings.model}"
        self.vector_dict.setdefault(vector_key, None)
        if self.vector_dict[vector_key] is None:
            self.vector_dict[vector_key] = PGVector(
                connection=SQLALCHEMY_DATABASE_URL,
                collection_name=collection_name,
                embeddings=embeddings,
                create_extension=False
            )
        return self.vector_dict[vector_key]

    def get_vector(self, collection_name: str, embeddings: OllamaEmbeddings) -> PGVector:
        vector_key = f"{collection_name}_{embeddings.model}"
        vector_store = self.vector_dict.get(vector_key)
        if vector_store is None:
            vector_store = self.__create_vector(collection_name, embeddings)
        return vector_store


if __name__ == "__main__":
    vector = Vector()
    vector.get_vector(
        collection_name="default",
        embeddings=OllamaEmbeddings(model="bge-m3", base_url="http://localhost:11434")
    )
