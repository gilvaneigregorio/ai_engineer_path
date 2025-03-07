import csv
import time
from itertools import islice
from typing import Dict, Generator, List

from ai.vectordb.base import DEFAULT_COLLECTION
from ai.vectordb.pgvector.pgvector import PGVector
from migrations.migrations import Migration
from utils.logging import logger
from utils.paths import get_root_path
from utils.relational_database import get_session


def chunk_reader(reader, chunk_size: int = 10000) -> Generator[List[Dict], None, None]:
    """Read CSV in chunks of specified size"""
    while True:
        chunk = list(islice(reader, chunk_size))
        if not chunk:
            break
        yield chunk


def count_lines(file_path: str) -> int:
    with open(file_path, "r", encoding="utf-8") as file:
        return sum(1 for _ in file) - 1  # -1 to exclude header row


Migration().run()

start_time = time.time()
file_path = f"{get_root_path()}/resources/full_dataset.csv"
total_lines = count_lines(file_path)

with open(file_path, "r", encoding="utf-8") as file:
    reader = csv.DictReader(file)

    i = 0
    for chunk in chunk_reader(reader, chunk_size=10000):
        db_session = next(get_session())
        vector_db = PGVector(db_session)
        vector_db.add(
            collection_name=DEFAULT_COLLECTION,
            texts=[row["NER"] for row in chunk],
            metadatas=chunk,
            ids=[row[""] for row in chunk],
        )

        db_session.close()
        i += len(chunk)
        perc = (i / total_lines) * 100
        logger.info(f"{i}/{total_lines} ({perc:.2f}%) rows inserted")

end_time = time.time()
logger.info(f"Insertion finished in {end_time - start_time:.2f} seconds")
