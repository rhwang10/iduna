import os
import redis
import hashlib

import urllib.parse as urlparse

class RedisClient:

    def __init__(self):
        endpoint_url = os.environ.get("REDIS_URL", "redis://127.0.0.1:6379")
        url = urlparse.urlparse(endpoint_url)
        self.client = redis.Redis(host=url.hostname, port=url.port, password=url.password)

    def set(self, key, expiration):
        return self.client.set(key, 'true', ex=expiration)

    def exists(self, key):
        return self.client.get(key)

    @staticmethod
    def key(user_id, msg_id):
        raw_key = f"{user_id}_{msg_id}"
        return hashlib.sha512(str.encode(raw_key)).hexdigest()
