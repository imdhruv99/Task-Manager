import json
import logging
import redis
from flask import current_app

logger = logging.getLogger(__name__)

def get_redis_client():
    """Get Redis client."""
    redis_url = current_app.config['REDIS_URL']
    return redis.from_url(redis_url)

def cache_get(key):
    """Get value from cache."""
    try:
        client = get_redis_client()
        data = client.get(key)
        if data:
            return json.loads(data)
        return None
    except Exception as e:
        logger.error(f"Redis cache get error: {str(e)}")
        return None

def cache_set(key, value, timeout=300):
    """Set value in cache."""
    try:
        client = get_redis_client()
        client.setex(key, timeout, json.dumps(value))
        return True
    except Exception as e:
        logger.error(f"Redis cache set error: {str(e)}")
        return False

def cache_delete(key):
    """Delete value from cache."""
    try:
        client = get_redis_client()
        client.delete(key)
        return True
    except Exception as e:
        logger.error(f"Redis cache delete error: {str(e)}")
        return False

def cache_flush_all():
    """Flush all cache."""
    try:
        client = get_redis_client()
        client.flushall()
        return True
    except Exception as e:
        logger.error(f"Redis cache flush error: {str(e)}")
        return False
