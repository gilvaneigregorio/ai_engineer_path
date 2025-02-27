from typing import Any, Dict, List, Optional

import chromadb
from chromadb import Collection, QueryResult

from ai.embeddings import Embedding

DEFAULT_COLLECTION = "default"


class VectorDB:
    def __init__(
        self,
        embedding_model: Embedding = Embedding(),
        host: str = "chromadb",
        port: str = "8000",
    ):
        self.client = chromadb.HttpClient(host=host, port=port)
        self.embedding_model = embedding_model

    def get_or_create_collection(self, name: str) -> Collection:
        return self.client.get_or_create_collection(name=name)

    def add(
        self,
        collection: Collection,
        texts: List[str],
        ids: List[str],
        metadatas: Optional[List[Dict[str, Any]]] = None,
    ):
        embeddings = self.embedding_model.encode(texts)
        collection.add(
            embeddings=embeddings, documents=texts, metadatas=metadatas, ids=ids
        )

    def search(
        self,
        collection: Collection,
        query: str,
        top_k: int = 10,
    ) -> QueryResult:
        query_embedding = self.embedding_model.encode(query)
        return collection.query(query_embeddings=query_embedding, n_results=top_k)
