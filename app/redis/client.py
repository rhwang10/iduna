import os
import redis
import hashlib
import time

import urllib.parse as urlparse

class RedisClient:

    def __init__(self):
        endpoint_url = os.environ.get("REDIS_URL", "redis://127.0.0.1:6379")
        url = urlparse.urlparse(endpoint_url)
        self.client = redis.Redis(host=url.hostname, port=url.port, password=url.password)

        # Default to every 10 minutes, todo make this configurable
        self.DEFAULT_INTERVAL = 600

        # Default to 5 tokens
        self.DEFAULT_REFILL = 1

    def _set(self, key, val, expiration):
        return self.client.set(key, val, ex=expiration)

    def _exists(self, key):
        return self.client.get(key)

    def _get(self, key, default_value=None):
        val = self.client.get(key)

        return val if val is not None else default_value

    def checkMessage(self, userId, messageId):
        print(f"Checking rate limiting for user id {userId} and message id {messageId}")
        currentTime = time.time()

        refillKey = self._hashKey(userId, messageId) + "_last_reset"
        bucketKey = self._hashKey(userId, messageId) + "_tokens"

        lastRefilled = float(self._get(refillKey, currentTime))

        # If the current time minus last refilled is 0 - its the first request. We need to add both keys
        if (currentTime - lastRefilled == 0) or (currentTime - lastRefilled) >= self.DEFAULT_INTERVAL:
            # expire refill tokens every day to clean up old messages
            self._set(bucketKey, self.DEFAULT_REFILL, 86400)
            self._set(refillKey, currentTime, 86400)
        else:
            tokens_left = int(self._get(bucketKey))

            if tokens_left < 1:
                return False

        self.client.decr(bucketKey, amount=1)
        return True

    def _hashKey(self, userId, msgId):
        raw_key = f"{userId}_{msgId}"
        return hashlib.sha512(str.encode(raw_key)).hexdigest()
