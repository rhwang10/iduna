from cachetools import TTLCache
from datetime import datetime, timedelta

from app.sql.users import (
    get_user_by_discord_id
)

class UserCache(TTLCache):
    def __init__(self, db):
        DEFAULT_MAX_SIZE=100
        DEFAULT_TTL = timedelta(hours=12)
        super().__init__(DEFAULT_MAX_SIZE, DEFAULT_TTL, timer=datetime.now)
        self.db = db


    def __missing__(self, key):
        print(f"Refreshing {key} to cache")
        user = get_user_by_discord_id(self.db, key)
        self[key] = user
        return user
