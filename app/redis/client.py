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
        self.DEFAULT_INTERVAL = 3

        # Default to 5 tokens
        self.DEFAULT_REFILL = 1

    def _set(self, key, val, expiration):
        return self.client.set(key, val, ex=expiration)

    def _exists(self, key):
        return self.client.get(key)

    def _get(self, key, default_value=None):
        val = self.client.get(key)

        return val if val is not None else default_value

    def _updateMessageHistory(self, userId, currentTime, messageId):
        ssName = self._hashKey(userId)
        self.client.zrem(ssName, messageId)
        self.client.zadd(ssName, {messageId: currentTime})

    def rankMessages(self, userId, availableMessages):

        idToMessage = {m.id: m for m in availableMessages}

        ssName = self._hashKey(userId)

        sortedMessageHistory = self.client.zrange(ssName, 0, -1, desc=False, withscores=True)

        prevMessageIds = list(map(lambda x: int(x[0]), sortedMessageHistory))

        messagesToClean = set(prevMessageIds).difference(idToMessage.keys())
        for idToDelete in messagesToClean:
            print(f"Deleting messageId {idToDelete} from {ssName} sorted set")
            self.client.zrem(ssName, idToDelete)

        orderedCandidates = []
        print(sortedMessageHistory)
        for candidateId, last_sent in sortedMessageHistory:
            try:
                orderedCandidates.append(idToMessage[int(candidateId)])
                del idToMessage[int(candidateId)]
            except KeyError:
                print(f"Did not find {candidateId} in the available messages!")

        unsentMessages = [v for k, v in idToMessage.items()]

        print([m.id for m in unsentMessages])
        orderedCandidates.extend(unsentMessages)

        print([m.id for m in orderedCandidates])
        for candidateMessage in orderedCandidates:
            yield candidateMessage


    def checkMessage(self, userId, messageId):
        print(f"Checking rate limiting for user id {userId} and message id {messageId}")
        currentTime = time.time()
        rawKey = f"{userId}_{messageId}"

        refillKey = self._hashKey(rawKey) + "_last_reset"
        bucketKey = self._hashKey(rawKey) + "_tokens"

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
        # Update/Add the message to the user's sorted set message history
        self._updateMessageHistory(userId, currentTime, messageId)
        return True

    def _hashKey(self, rawKey):
        return hashlib.sha512(str.encode(rawKey)).hexdigest()
