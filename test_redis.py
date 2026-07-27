from app.core.redis_client import redis_client

redis_client.set(
    "test_key",
    "KnowledgeVault Redis Working"
)

print(
    redis_client.get("test_key")
)