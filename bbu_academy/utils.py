from pathlib import Path


def remove(path: Path):
    if path and path.exists():
        if path.is_dir():
            clear_directory(path)
            path.rmdir()
        else:
            path.unlink()


def clear_directory(path: Path):
    for item in path.iterdir():
        if item.is_dir():
            clear_directory(item)
            item.rmdir()
        elif item.is_file():
            item.unlink()
