from pathlib import Path


def get_root_path() -> str:
    path = Path(__file__).parent.parent.parent
    return str(path.absolute())
