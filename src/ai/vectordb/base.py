from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

from chromadb import QueryResult

from ai.models.embeddings import EmbeddingModel

DEFAULT_COLLECTION = "default"


class BaseVectorDB(ABC):
    def __init__(self, embedding_model: EmbeddingModel = EmbeddingModel()):
        self.embedding_model = embedding_model

    @abstractmethod
    def add(
        self,
        collection_name: str,
        texts: List[str],
        ids: List[str],
        metadatas: Optional[List[Dict[str, Any]]] = None,
    ):
        pass

    @abstractmethod
    def search(
        self,
        collection_name: str,
        query: str,
        top_k: int = 10,
    ) -> QueryResult:
        pass
