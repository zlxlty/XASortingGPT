import dotenv
from langchain import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import HumanMessagePromptTemplate, AIMessagePromptTemplate, SystemMessagePromptTemplate, ChatPromptTemplate
from typing import List, Any, Awaitable

from GPTParser.defines import Dict
from .model import Message, MessagePrompt, SortingPrompt
from .defines import *
import asyncio

class Parser(object):
    def __call__(self):
        raise NotImplementedError("Parse method not implemented")

class InterestParser(Parser):
    """ Messages[34] to Messages[49] """
    
    async def __call__(self, kwargs: Dict[str, Any]) -> str:
        if MESSAGES not in kwargs: return ""
        interests = []
        messages = kwargs[MESSAGES]
        for message in messages:
            if message.role == 'user':
                interests += (message.content.split(','))
                
        await asyncio.sleep(0)
        return ",".join(interests)

class GPTParser(Parser):
    template = Message(role=ROLE_USR, content=f"Hello XA! {{{MESSAGES}}}")
    def __init__(self):
        chat = ChatOpenAI(model="gpt-3.5-turbo-16k-0613", openai_api_key=dotenv.dotenv_values()['OPENAI_API_KEY'])
        prompt = self.__create_prompt()
        self.chain = LLMChain(llm=chat, prompt=prompt)

    def __create_prompt(self):
        from_template = {
            ROLE_USR: HumanMessagePromptTemplate.from_template,
            ROLE_BOT: AIMessagePromptTemplate.from_template,
            ROLE_SYS: SystemMessagePromptTemplate.from_template   
        }
        
        return ChatPromptTemplate.from_messages([from_template[self.template.role](self.template.content)])
    
    def is_kwargs_valid(self, kwargs: Dict[str, Any]):
        raise NotImplementedError("Prompt argument check not implemented")
    
    async def __call__(self, kwargs: Dict[str, str]) -> str:
        self.is_kwargs_valid(kwargs)
        return await self.chain.arun(**kwargs)

class CharacterGPTParser(GPTParser):
    """ Messages[6] to Messages[33] """
    template = PROMPT_TEMPLATE[SEG_CHARACTER]
    
    def is_kwargs_valid(self, kwargs: Dict[str, Any]) -> bool:
        MessagePrompt(**kwargs)
        
    
class StoryGPTParser(CharacterGPTParser):
    """ Messages[50] to Messages[63] """
    template = PROMPT_TEMPLATE[SEG_STORY]
    
    
class SortingResultParser(GPTParser):
    template = PROMPT_TEMPLATE[SORTING_HAT]
    
    def is_kwargs_valid(self, kwargs: Dict[str, Any]) -> bool:
        SortingPrompt(**kwargs)


ParserMap = {
    SEG_INTEREST: InterestParser(),
    SEG_CHARACTER: CharacterGPTParser(),
    SEG_STORY: StoryGPTParser(),
    SORTING_HAT: SortingResultParser()
}    


async def aparse(parser_type: str, kwargs: Dict[str, Any]) -> str:
    print(parser_type)
    if parser_type not in ParserMap:
        return ""
    
    parser = ParserMap[parser_type]
    return await parser(kwargs)


if __name__ == '__main__':
    import csv
    from .utils import string_to_messages
    
    with open('./data/XASortingProfile.csv', 'r') as file:
        reader = csv.reader(file)
        header = next(reader)  # Read the header row
        
        row = next(reader)
        raw_messages = row[header.index("conversations")]
        messages = string_to_messages(raw_messages)
        interests = InterestParser()(messages[34:50])
        print(interests)
