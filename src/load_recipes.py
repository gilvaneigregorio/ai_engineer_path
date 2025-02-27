from dotenv import load_dotenv

from ai.vectordb import DEFAULT_COLLECTION, VectorDB
from utils.loaders import CSVLoader
from utils.logging import logging
from utils.paths import get_root_path

load_dotenv()

csv_loader = CSVLoader(f"{get_root_path()}/resources/full_dataset.csv")
vector_db = VectorDB()
collection = vector_db.get_or_create_collection(DEFAULT_COLLECTION)
for chunk in csv_loader.read_chunks(start_index=0, limit=None):
    logging.info(f"Adding {len(chunk)} rows to collection {DEFAULT_COLLECTION}")
    vector_db.add(
        collection=collection,
        texts=[row["NER"] for row in chunk],
        metadatas=chunk,
        ids=[row[""] for row in chunk],
    )
