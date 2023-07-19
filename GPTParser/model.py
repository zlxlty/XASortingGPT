from typing import List
from pydantic import BaseModel, validator
from .defines import *

class Message(BaseModel):
    role: str
    content: str
    
    @validator('role')
    @classmethod
    def role_is_valid(cls, v):
        if v not in [ROLE_USR, ROLE_BOT, ROLE_SYS]:
            raise ValueError('Invalid role')
        return v
    
    
class MessagePrompt(BaseModel):
    messages: List[Message]
    
class SortingPrompt(BaseModel):
    name: str
    character: str
    interest: str
    story: str