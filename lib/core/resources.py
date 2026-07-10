from pathlib import Path
import sys


def resource_path(rel_path: str | Path) -> Path:
    rel = Path(rel_path)
    base = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parents[1]))
    return base / rel
