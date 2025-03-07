from pydantic import BaseModel


class VectorQueryResult(BaseModel):
    id: str
    text: str
    metadata: dict
    embedding: list
