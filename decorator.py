from typing import List, Awaitable
import tinydb
from functools import wraps
import asyncio
from defines import *

def memoize_with_db(db, fields):
    def memoize_with_db_inner(function: Awaitable):
        @wraps(function)
        async def memoized_function(*args, **kwargs) -> List[str]:
            if USER_ID not in kwargs:
                
                raise ValueError("User ID not provided")
            
            UserQuery = tinydb.Query()
            user = db.get(UserQuery.user_id == kwargs[USER_ID])
            if not user or not set(fields).issubset(set(user.keys())):
                
                not user and db.insert({USER_ID: kwargs[USER_ID]})
                result = await function(*args, **kwargs)
                db.upsert(result, UserQuery.user_id == kwargs[USER_ID])
                return result
            await asyncio.sleep(0)
            return [user[field] for field in fields]
                
        
        return memoized_function
    return memoize_with_db_inner