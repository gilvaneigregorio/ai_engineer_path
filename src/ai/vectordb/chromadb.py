from typing import Any, Dict, List, Optional

import chromadb

from ai.models.embeddings import EmbeddingModel
from ai.vectordb.base import BaseVectorDB
from ai.vectordb.schemas import VectorQueryResult

DEFAULT_COLLECTION = "default"


class ChromaDB(BaseVectorDB):
    def __init__(
        self,
        embedding_model: EmbeddingModel = EmbeddingModel(),
        host: str = "chromadb",
        port: str = "8000",
    ):
        super().__init__(embedding_model)
        self.client = chromadb.HttpClient(host=host, port=port)

    def add(
        self,
        collection_name: str,
        texts: List[str],
        ids: List[str],
        metadatas: Optional[List[Dict[str, Any]]] = None,
    ):
        collection = self.client.get_or_create_collection(collection_name)
        embeddings = self.embedding_model.encode(texts)
        collection.add(
            embeddings=embeddings, documents=texts, metadatas=metadatas, ids=ids
        )

    def search(
        self,
        collection_name: str,
        query: str,
        top_k: int = 10,
    ) -> VectorQueryResult:
        collection = self.client.get_or_create_collection(collection_name)
        query_embedding = self.embedding_model.encode(query)
        query_result = collection.query(
            query_embeddings=query_embedding, n_results=top_k
        )

        return [
            VectorQueryResult(
                id=result.id,
                text=result.text,
                metadata=result.metadata,
                embedding=result.embedding,
            )
            for result in query_result
        ]
