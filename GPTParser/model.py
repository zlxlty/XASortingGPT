from textwrap import dedent
from typing import List, Sequence

from pydantic import BaseModel, Field, validator

from .define import *


class Message(BaseModel):
    role: str
    content: str

    @validator("role")
    @classmethod
    def role_is_valid(cls, v):
        if v not in [ROLE_USR, ROLE_BOT, ROLE_SYS]:
            raise ValueError("Invalid role")
        return v

    @validator("content")
    @classmethod
    def format_content(cls, v):
        return dedent(v).strip("/n")


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
    percentage: float = Field(
        ..., description="A decimal value in the text before % sign"
    )