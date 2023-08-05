import os
import redis


RC_DB_TYPE = os.getenv("RC_DB_TYPE", "strict")

if RC_DB_TYPE == "strict":
    READ_HOST = os.getenv("READ_HOST", "localhost")
    READ_PORT = int(os.getenv("READ_PORT", "6379"))
    READ_DB = int(os.getenv("READ_DB", "0"))
    WRITE_HOST = os.getenv("WRITE_HOST", "localhost")
    WRITE_PORT = int(os.getenv("WRITE_PORT", "6379"))
    WRITE_DB = int(os.getenv("WRITE_DB", "0"))
    r = redis.StrictRedis(host='localhost', port=6379, db=0)
    w = redis.StrictRedis(host='localhost', port=6379, db=0)
elif RC_DB_TYPE == "url":
    REDIS_READ_URL = os.getenv("REDIS_READ_URL", "redis://localhost")
    REDIS_WRITE_URL = os.getenv("REDIS_WRITE_URL", "redis://localhost")
    r = redis.from_url(REDIS_READ_URL)
    w = redis.from_url(REDIS_WRITE_URL)
else:
    raise
