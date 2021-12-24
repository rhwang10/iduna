# iduna
HTV's API layer

# Setup
- Setup local postgres and export env variable DATABASE_URL as `postgres://localhost:5432`

- Setup local Redis server according to instructions https://redis.io/topics/quickstart and start with `redis-server`

- Run `sh run.sh` to start the server

# Message rate limiting
Token bucket rate limiting algorithm

1. (TODO) Based on the message's cap. Check if the current time minus the last time the bucket was refilled is greater than the interval. If so, refill the bucket.

Maintain two keys:
1) Hash(userId, messageId) + last_reset -> Epoch seconds
2) Hash(userId, messageId) + tokens -> Integer

If the interval has not been surpassed yet, get the number of tokens in the bucket.
If there are no tokens left, return false

Decrement the number of tokens and return true
