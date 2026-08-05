"""
Pytest configuration for the KnowledgeVault test suite.

Sets required environment variables before any app module is imported.
This ensures the JWT_SECRET validator (>= 32 chars) does not break test
collection when the local .env contains a short development secret.
"""
import os

# Override JWT_SECRET so the >=32-char validator passes during test imports.
# The local .env may contain a short dev value (e.g. 'supersecretkey').
# os.environ takes precedence over the .env file in pydantic-settings v2.
os.environ["JWT_SECRET"] = "test-only-jwt-secret-that-is-32-chars-x"

# Ensure DATABASE_URL is present so Settings() can be instantiated even
# without a real database. Tests that actually hit the DB are integration
# tests and are not in scope here.
os.environ.setdefault(
    "DATABASE_URL",
    "postgresql://test:test@localhost:5432/test",
)
