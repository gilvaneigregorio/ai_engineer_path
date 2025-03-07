CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS embeddings (
    id SERIAL PRIMARY KEY,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    text TEXT,
    embedding vector(384),
    metadata_dict JSONB,
    collection TEXT
);

CREATE INDEX IF NOT EXISTS embeddings_embedding_hnsw_idx
ON embeddings
USING hnsw (embedding vector_l2_ops);

CREATE INDEX IF NOT EXISTS embeddings_collection_idx
ON embeddings (collection);