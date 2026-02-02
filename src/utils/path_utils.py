from pathlib import Path


def get_project_root() -> Path:
    """
    Returns project root directory (one level above src/)
    """
    return Path(__file__).resolve().parents[2]


def project_path(*paths) -> Path:
    """
    Build path relative to project root
    """
    return get_project_root().joinpath(*paths)
