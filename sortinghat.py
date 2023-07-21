from typing import List, Awaitable
import tinydb
from functools import wraps
import asyncio
from defines import *
import GPTParser as gp
from typing import List, Awaitable, Dict, Any
from utils import list_to_dict

class SortingHat(object):
    
    summarize_fields = [
        gp.SEG_CHARACTER,
        gp.SEG_INTEREST,
        gp.SEG_STORY
    ]
    
    judge_fields = [
        gp.STR_QUAL_JUDGEMENT
    ]
    
    format_fields = [
        gp.STR_GPT_FUNC_OUTPUT
    ]
    
    def __init__(self, user_id, username):
        self.user_id = user_id
        self.username = username
        
    @classmethod
    def put_on(cls, user_id, username):
        return cls(user_id, username)
    
    def read_mind(self, message_segments, db):
        self.message_segments = message_segments
        self.db = db
    
    async def decide(self) -> bool:
        try:
            summarized_segments = await self.summarize_user_info(self.message_segments)
            summarized_segments[gp.STR_USERNAME] = self.username
            
            raw_judgement = await self.judging_user_quality(summarized_segments)
            await self.format_judgment_output(raw_judgement)
            # print(formatted_output)
            return True

        except Exception as e:
            # print(f"User {self.username} failed to be sorted")
            await asyncio.sleep(0)
            return False 
    
    def _memoize_with_db(fields):
        def memoize_with_db_inner(method: Awaitable):
            @wraps(method)
            async def memoized_method(self, *args, **kwargs) -> List[str]:
                
                UserQuery = tinydb.Query()
                user = self.db.get(UserQuery.user_id == self.user_id)
                if not user or not set(fields).issubset(set(user.keys())):
                    print(f"User ({self.user_id}): db cache miss in {fields}! Calculating...")
                    
                    not user and self.db.insert({USER_ID: self.user_id})
                    result = await method(self, *args, **kwargs)
                    self.db.upsert(result, UserQuery.user_id == self.user_id)
                    print(f"User ({self.user_id}): db cache inserted in {fields}!")
                    
                    return result
                
                print(f"User ({self.user_id}): db cache hit in {fields}!")
                await asyncio.sleep(0)
                return list_to_dict(fields, [user[field] for field in fields])
                    
            
            return memoized_method
        return memoize_with_db_inner
    
    @_memoize_with_db(summarize_fields)
    async def summarize_user_info(self, message_segments) -> Dict[str, Any]:
        parsing_tasks = [
            gp.aparse(
                segment_name, 
                {gp.STR_MESSAGES: message_segments[segment_name]}
            ) for segment_name in self.summarize_fields
        ]
        
        parsed_segments = await asyncio.gather(*parsing_tasks)
        
        return list_to_dict(self.summarize_fields, parsed_segments)
    
    @_memoize_with_db(judge_fields)
    async def judging_user_quality(self, summarized_segments) -> Dict[str, Any]:
        raw_judgement = await gp.aparse(self.judge_fields[0], summarized_segments)
        return list_to_dict(self.judge_fields, [raw_judgement])
    
    
    @_memoize_with_db(format_fields)
    async def format_judgment_output(self, judgement) -> Dict[str, Any]:
        formatted_output = await gp.aparse(self.format_fields[0], judgement)
        serialized_output = [dict(attrModel) for attrModel in formatted_output.attributes]
        return list_to_dict(self.format_fields, [serialized_output])
    
    