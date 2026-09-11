import json
from pathlib import Path
from django.conf import settings

_CATALOG_PATH = Path(settings.BASE_DIR) / "exercises" / "data" / "workout_guide_catalog.json"
_cache = None


def load_catalog():
    # Lee el catálogo de workout-guide una sola vez y lo cachea en memoria
    global _cache
    if _cache is None:
        with open(_CATALOG_PATH, encoding="utf-8") as f:
            data = json.load(f)
        _cache = sorted(
            [{"slug": item["slug"], "name": item["name"]} for item in data],
            key=lambda item: item["name"],
        )
    return _cache