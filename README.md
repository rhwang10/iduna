# Iduna
HTV's API layer - exposes endpoints for message selection, consumed by HTV's discord bot, Elsa.

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

# Message selection

Iduna uses the least recently used principle to decide what message should be sent. A Redis sorted set is used to keep track of the timestamp a message was last sent to a user. The name of the sorted set is a hash of the userId, so each user will effectively have their own sorted set of messages.

Name: hash(userId)
Key: Epoch seconds
Value: messageId

When all available messages are loaded into memory for a user, the following alogrithm will apply:

1. Get all values of the sorted set, and take the set difference with the available messages. If the set difference is not empty, pick a random message from the diff and check its send availability.

2. If the set difference is empty, that means that all available messages have been sent at least once. We will loop from least recent to most recent, and check send availability. When we find a message we can send, we will update its score in the sorted set to the current epoch second.

3. We will need a way to "clean" the sorted set, and remove messageIds that have been deleted from the database. Additionally, we don't want to remove messageIds that have been just deactivated.
