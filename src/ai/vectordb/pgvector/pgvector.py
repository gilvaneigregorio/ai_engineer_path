import time
from typing import Any, Dict, List, Optional

from sqlalchemy.orm import Session

from ai.models.embeddings import EmbeddingModel
from ai.vectordb.base import BaseVectorDB
from ai.vectordb.pgvector.models import Embedding
from ai.vectordb.pgvector.repositories import EmbeddingsRepository
from ai.vectordb.schemas import VectorQueryResult
from utils.logging import logger


class PGVector(BaseVectorDB):
    def __init__(
        self, db_session: Session, embedding_model: EmbeddingModel = EmbeddingModel()
    ):
        super().__init__(embedding_model)
        self.repository = EmbeddingsRepository(db_session)

    def add(
        self,
        collection_name: str,
        texts: List[str],
        ids: List[str],
        metadatas: Optional[List[Dict[str, Any]]] = None,
    ):
        start_time = time.time()
        embeddings = self.embedding_model.encode(texts)
        logger.info(f"Encoding time: {time.time() - start_time:.2f} seconds")
        start_time = time.time()
        embedding_objects = [
            Embedding(
                text=text,
                embedding=embeddings[idx],
                metadata_dict=metadatas[idx] if metadatas else {"chunk_id": idx},
                collection=collection_name,
            )
            for idx, text in enumerate(texts)
        ]

        # Bulk insert
        self.repository.db_session.bulk_save_objects(embedding_objects)
        self.repository.db_session.commit()
        logger.info(f"Insertion time: {time.time() - start_time:.2f} seconds")

    def search(
        self,
        collection_name: str,
        query: str,
        top_k: int = 10,
    ) -> List[VectorQueryResult]:
        embedding_vector = self.embedding_model.encode([query])[0]
        embeddings = Embedding.query(
            self.repository,
            embedding_vector,
            collection_name,
            top_k,
        )

        return [
            VectorQueryResult(
                id=str(embedding.id),
                text=embedding.text,
                metadata=embedding.metadata_dict,
                embedding=embedding.embedding,
            )
            for embedding in embeddings
        ]
