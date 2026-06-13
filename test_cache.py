from app.services.cache_service import CacheService


CacheService.set(
    "note_search:test",
    ["note1", "note2"]
)

print(
    CacheService.get(
        "note_search:test"
    )
)