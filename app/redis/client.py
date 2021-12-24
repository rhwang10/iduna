import os
import redis
import hashlib

class RedisClient:

    def __init__(self):
        endpoint_url = os.environ.get("REDIS_ENDPOINT_URL", "127.0.0.1:6379")
        REDIS_HOST, REDIS_PORT = tuple(endpoint_url.split(":"))
        REDIS_PASSWORD = os.environ.get("REDIS_PASSWORD", None)
        self.client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD)

    def set(self, key, expiration):
        return self.client.set(key, 'true', ex=expiration)

    def exists(self, key):
        return self.client.get(key)

    @staticmethod
    def key(user_id, msg_id):
        raw_key = f"{user_id}_{msg_id}"
        return hashlib.sha512(str.encode(raw_key)).hexdigest()
