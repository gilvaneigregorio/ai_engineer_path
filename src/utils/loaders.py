# CSV loaderimport csv
import csv
from pathlib import Path
from typing import Any, Dict, Generator, List


class CSVLoader:
    def __init__(self, file_path: str, chunk_size: int = 100):
        self.chunk_size = chunk_size
        self.file_path = Path(file_path)
        if not self.file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

    def read_chunks(
        self, start_index: int = 0, limit: int = None
    ) -> Generator[List[Dict[str, Any]], None, None]:
        with open(self.file_path, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            chunk = []
            current_index = 0
            rows_read = 0

            # Skip rows until start_index
            for _ in range(start_index):
                try:
                    next(reader)
                    current_index += 1
                except StopIteration:
                    return

            for row in reader:
                # Stop reading if limit is reached
                if limit and rows_read >= limit:
                    break

                chunk.append(row)
                rows_read += 1
                # Yield chunk when it reaches the desired size
                if len(chunk) >= self.chunk_size:
                    yield chunk
                    chunk = []

            # Yield the last chunk if it's not empty
            if chunk:
                yield chunk
