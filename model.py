import re
from typing import List, Optional, Union

from pydantic import BaseModel, validator


# class Student(BaseModel):
#     name: str
#     email: str
#     characteristics: str
#     interests: List[str]
#     story: str
#     house: Optional[str]
#     reason: Optional[str]

#     @validator("email")
#     @classmethod
#     def email_is_valid(cls, v):
#         if not re.match(r"[^@]+@[^@]+\.[^@]+", v):
#             raise ValueError("Invalid email address")
#         return v


class Message(BaseModel):
    role: str
    content: str

    @validator("role")
    @classmethod
    def role_is_valid(cls, v):
        if v not in ["user", "assistant", "system"]:
            raise ValueError("Invalid role")
        return v
