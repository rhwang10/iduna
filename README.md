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
```
Name: hash(userId)
Score: Epoch seconds
Value: messageId
```
When all available messages are loaded into memory for a user, the following algorithm will apply:

1. Get all values of the sorted set, and take the set difference with the available messages. Remove all of the deleted messages from the sorted set

2. Iterate through the sorted message history, and append the Message model object to the orderedCandidates, and delete the key from the mapping of available message Id to available messages.

3. After all of the valid message history has been prioritized, add the remaining messages in the set of available messages from Postgres (this might include messages that are being sent for the first time). Then yield messages one by one, until one is chosen.
