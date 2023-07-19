from typing import List, Dict
from .model import Message
from .defines import *

def string_to_messages(raw_messages_string: str) -> List[Message]:
    import ast
    raw_messages = ast.literal_eval(raw_messages_string)
    return [Message(**m) for m in raw_messages]

def segment_messages(messages: List[Message], segments: Dict[str, List[int]] = MESSAGE_SEGMENT) -> Dict[str, List[Message]]:
    return {segment: messages[indices[0]: indices[1]+1] for segment, indices in segments.items()}