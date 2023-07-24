import asyncio
from functools import wraps
from typing import Any, Awaitable, Dict, List
from copy import deepcopy
import tinydb

import GPTParser as gp
from define import *
from utils import list_to_dict


class SortingHat(object):
    summarize_fields = [gp.SEG_CHARACTER, gp.SEG_INTEREST, gp.SEG_STORY]

    # judge_fields = [gp.STR_QUAL_JUDGEMENT]
    judge_fields = gp.ATTRIBUTE_NAMES_IN_HOUSE

    format_fields = gp.HOUSE_NAMES

    sorting_fields = [gp.STR_SORTING]

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
            await self.add_basic_info()
            summarized_segments = await self.summarize_user_info(self.message_segments)
            summarized_segments[gp.STR_USERNAME] = self.username

            raw_judgements = await self.judging_user_quality(summarized_segments)
            
            await self.format_judgment_output(raw_judgements)
            return True

        except Exception as e:
            print(f"User {self.username} failed to be sorted due to exception:")
            print(e)
            print("="*20)
            await asyncio.sleep(0)
            return False

    def _memoize_with_db(fields):
        def memoize_with_db_inner(method: Awaitable):
            @wraps(method)
            async def memoized_method(self, *args, **kwargs) -> List[str]:
                UserQuery = tinydb.Query()
                user = self.db.get(UserQuery.user_id == self.user_id)
                if not user or not set(fields).issubset(set(user.keys())):
                    print(
                        f"User ({self.user_id}): db cache miss in {fields}! Calculating..."
                    )

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
    
    @_memoize_with_db([gp.STR_USERNAME])
    async def add_basic_info(self):
        await asyncio.sleep(0)
        return {gp.STR_USERNAME: self.username}

    @_memoize_with_db(summarize_fields)
    async def summarize_user_info(self, message_segments) -> Dict[str, Any]:
        parsing_tasks = [
            gp.aparse(segment_name, {gp.STR_MESSAGES: message_segments[segment_name]})
            for segment_name in self.summarize_fields
        ]

        parsed_segments = await asyncio.gather(*parsing_tasks)

        return list_to_dict(self.summarize_fields, parsed_segments)

    @_memoize_with_db(judge_fields)
    async def judging_user_quality(self, summarized_segments) -> Dict[str, Any]:
        
        parsing_tasks = []
        
        for attribute_name in self.judge_fields:
            summarized_segments[gp.STR_ATTRIBUTE] = attribute_name
            await asyncio.sleep(0.2)
            parsing_tasks.append(gp.aparse(gp.STR_QUAL_JUDGEMENT, deepcopy(summarized_segments))) 
        
        parsed_judgement = await asyncio.gather(*parsing_tasks)
        
        # raw_judgement = await gp.aparse(self.judge_fields[0], summarized_segments)
        return list_to_dict(self.judge_fields, parsed_judgement)

    @_memoize_with_db(format_fields)
    async def format_judgment_output(self, judgements) -> Dict[str, Any]:
        parsing_tasks = []
        
        for judgement in judgements.values():
            parsing_tasks.append(gp.aparse(gp.STR_GPT_FUNC_OUTPUT, {gp.STR_QUAL_JUDGEMENT: judgement}))
            
        parsed_output = await asyncio.gather(*parsing_tasks)
        
        serialized_output = [
            attrModel.percentage for attrModel in parsed_output
        ]
        
        return list_to_dict(self.format_fields, serialized_output)

    # @_memoize_with_db(sorting_fields)
    # async def calculating_house_preference(self, formatted_output) -> Dict[str, Any]:
    #     house_preference = {house_name: 0 for house_name in gp.HOUSE_NAMES}

    #     for attribute_model in formatted_output[gp.STR_GPT_FUNC_OUTPUT]:
    #         attribute = attribute_model["attribute_name"]
    #         score = attribute_model["score"]
    #         house_name = gp.ATTRIBUTES_TO_HOUSE_NAMES[attribute]
    #         house_preference[house_name] += score

    #     house_preference_list = [
    #         (house_name, score) for house_name, score in house_preference.items()
    #     ]
    #     house_preference_list.sort(key=lambda x: x[1], reverse=True)

    #     await asyncio.sleep(0)
    #     return list_to_dict(self.sorting_fields, [house_preference_list])
