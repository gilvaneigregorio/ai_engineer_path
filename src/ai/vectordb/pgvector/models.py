from pgvector.sqlalchemy import Vector
from sqlalchemy import JSON, TIMESTAMP, Index, Integer, Text
from sqlalchemy.orm import mapped_column

from utils.relational_database import Base


class Embedding(Base):
    __tablename__ = "embeddings"
    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    created_at = mapped_column(
        TIMESTAMP(timezone=True), nullable=False, default="now()"
    )
    text = mapped_column(Text)
    embedding = mapped_column(Vector(384))
    metadata_dict = mapped_column(JSON)
    collection = mapped_column(Text)

    __table_args__ = (
        Index(
            "embeddings_embedding_hnsw_idx",
            "embedding",
            postgresql_using="hnsw",
            postgresql_ops={"embedding": "vector_l2_ops"},
        ),
    )

    @classmethod
    def create(
        cls,
        repository: any,
        text: str,
        embedding_vector: any,
        metadata_dict: dict,
        collection: str,
        commit: bool = True,
    ):
        embedding = cls(
            text=text,
            embedding=embedding_vector,
            metadata_dict=metadata_dict,
            collection=collection,
        )
        return repository.create(embedding, commit=commit)

    @classmethod
    def query(
        self, repository: any, embedding_vector: any, collection: str, top_k: int = 3
    ):
        return repository.list_by_l2_distance(embedding_vector, collection, top_k)
