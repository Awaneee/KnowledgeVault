import json
from pathlib import Path

from app.evaluation.models import BenchmarkQuery


class BenchmarkLoader:
    """
    Loads benchmark queries from JSON.

    The benchmark dataset intentionally lives outside the database so that:
    - it is version controlled
    - it is easy to edit
    - evaluation remains deterministic
    """

    @staticmethod
    def load(path: str | Path) -> list[BenchmarkQuery]:
        path = Path(path)

        if not path.exists():
            raise FileNotFoundError(
                f"Benchmark file not found: {path}"
            )

        with open(path, "r", encoding="utf-8") as file:
            raw = json.load(file)

        if not isinstance(raw, list):
            raise ValueError(
                "Benchmark dataset must be a JSON array."
            )

        return [
            BenchmarkQuery.model_validate(item)
            for item in raw
        ]