from sqlalchemy import select
from sqlalchemy.orm import Session

from ai.vectordb.pgvector.models import Embedding


class EmbeddingsRepository:
    def __init__(self, db_session: Session) -> None:
        self.db_session = db_session

    def create(self, embedding: Embedding, commit: bool = True) -> Embedding:
        self.db_session.add(embedding)
        if commit:
            self.db_session.commit()
            self.db_session.refresh(embedding)
        return embedding

    def list_by_l2_distance(self, embedding_vector, collection_name, top_k=3):
        stmt = (
            select(Embedding)
            .where(Embedding.collection == collection_name)
            .order_by(Embedding.embedding.l2_distance(embedding_vector))
            .limit(top_k)
        )
        return self.db_session.execute(stmt).scalars().all()
