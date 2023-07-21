from typing import List, Sequence
from pydantic import BaseModel, validator, Field
from .defines import *
from textwrap import dedent

class Message(BaseModel):
    role: str
    content: str
    
    @validator('role')
    @classmethod
    def role_is_valid(cls, v):
        if v not in [ROLE_USR, ROLE_BOT, ROLE_SYS]:
            raise ValueError('Invalid role')
        return v
    
    @validator('content')
    @classmethod
    def format_content(cls, v):
        return dedent(v).strip('/n')
    
    
class MessagePrompt(BaseModel):
    messages: List[Message]
    
class SortingPrompt(BaseModel):
    name: str
    character: str
    interest: str
    story: str
    
class CleaningPrompt(BaseModel):
    quality_judgement: str
    
class AttributeModel(BaseModel):
    attribute_name: str = Field(..., description="The name of an attribute")
    score: int = Field(..., description="The score given to this attribute in percentage")
    reasons: str = Field(..., description="The three reasons in Chinese that explain the score given to this attribute")
    
    @validator('attribute_name')
    @classmethod
    def attribute_name_is_valid(cls, v):
        if v not in ATTRIBUTE_NAMES:
            raise ValueError('Invalid attribute name')
        return v
    
class Attributes(BaseModel):
    attributes: Sequence[AttributeModel] = Field(..., description=f"All the {len(ATTRIBUTE_NAMES)} attributes in the text")