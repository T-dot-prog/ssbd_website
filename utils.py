"""
Utils function for ssbd web portal. It includes redis memory setup.
"""

import redis
from config import config
from logger import logger
import json

from typing_extensions import Any, Optional, Dict

class RedisMemory:
    def __init__(self,
        host: str = config.REDIS_HOST,
        port: int = config.REDIS_PORT,
        db: int = config.REDIS_DB,
        password: str = config.REDIS_PASSWORD ):
        
        try:
            self.redis = redis.Redis(
                host=host,
                port=port,
                db=db,
                password=password,
                decode_responses=True
            )
            logger.info(f"Connected to Redis at {host}:{port}")
        except redis.ConnectionError as e:
            logger.error(f"Failed to connect to Redis: {str(e)}")
            raise

    def load_info(self, key: str) -> Optional[Dict[str, Any]]:
        """Load info from redis database"""
        try:
            info = self.redis.get(name= key)
            if info:
                return json.loads(info)
            logger.debug("No Information is found for debug")
            return None
        except Exception as e:
            logger.error(f'Failed to load information according to this key: {e}')
            return None
        
    def save_info(self,key: str, info: Dict[str, str], ttl: Optional[int] = None) -> bool:
        """Send Information into redis database"""

        try:
            serilized_info = json.dumps(info)

            self.redis.set(name= key, value= serilized_info)

            if ttl:
                self.redis.expire(key, ttl)
            logger.debug(f'Saved information for key: {key}')
            return True
        except Exception as e:
            logger.error(f"Falied to save information: {e}")
            return False

    def close(self):
        """Close Redis Connection"""
        try:
            self.redis.close()
            logger.info('Closing Redis Connection')
        except Exception as e:
            logger.error(f'Failed to close redis connection: {e}')
            raise


redis_db = RedisMemory()