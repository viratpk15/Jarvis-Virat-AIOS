"""
Jarvis AIOS
-----------
Configuration Settings

Loads runtime configuration from environment variables. A `.env` file at the
project root is supported via python-dotenv. Secrets (JWT signing key) are
never hardcoded and must be provided through the environment.
"""

import os

from dotenv import load_dotenv

load_dotenv()

# JWT configuration
# Secret used to sign HS256 access tokens. MUST be set in the environment.
JWT_SECRET_KEY: str | None = os.getenv("JWT_SECRET_KEY")
# Signing algorithm. HS256 is required for the v1.0 Placement Edition.
JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
# Access token lifetime in hours.
JWT_ACCESS_TOKEN_EXPIRE_HOURS: int = int(os.getenv("JWT_EXPIRE_HOURS", "24"))

# Authentication database path (SQLite). Overridable for tests.
AUTH_DB_PATH: str = os.getenv("AUTH_DB_PATH", "./data/auth.db")

# Persistence database path (SQLite) for memory/session storage.
PERSISTENCE_DB_PATH: str = os.getenv("PERSISTENCE_DB_PATH", "./data/memory.db")

# Application version. Bump this when releasing.
APP_VERSION: str = os.getenv("APP_VERSION", "1.0.0")

# Rate limiting (in-memory, no Redis needed for v1.0)
# Login: strict — 5 requests per minute per IP
LOGIN_RATE_LIMIT: str = os.getenv("LOGIN_RATE_LIMIT", "5/minute")
# Register: strict — 3 requests per minute per IP
REGISTER_RATE_LIMIT: str = os.getenv("REGISTER_RATE_LIMIT", "3/minute")
# Chat: generous — 30 requests per minute per IP
CHAT_RATE_LIMIT: str = os.getenv("CHAT_RATE_LIMIT", "30/minute")
