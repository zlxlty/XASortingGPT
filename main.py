import csv

import GPTParser as gp
import asyncio
from defines import *


async def write_sorting_result(raw_messages_string: str) -> str:
        messages = gp.string_to_messages(raw_messages_string)
        message_segments = gp.segment_messages(messages)
        
        explorer_name = message_segments[gp.SEG_BASIC][1].content
        
        segment_to_parse = [
            gp.SEG_CHARACTER,
            gp.SEG_INTEREST,
            gp.SEG_STORY 
        ]
        
        parsing_tasks = [
            gp.aparse(
                segment_name, 
                {gp.MESSAGES: message_segments[segment_name]}
            ) for segment_name in segment_to_parse
        ]
    
        parsed_segments = await asyncio.gather(*parsing_tasks)
    
        result = await gp.aparse(gp.SORTING_HAT, {
            gp.NAME: explorer_name,
            gp.SEG_CHARACTER: parsed_segments[0],
            gp.SEG_INTEREST: parsed_segments[1],
            gp.SEG_STORY: parsed_segments[2]
        })
        
        print(result)
        
        write_result_to_csv(result)
        
def write_result_to_csv(result: str):
    pass

async def main():
    with open('/'.join([INPUT_FOLDER, CSV_FILENAME]), 'r') as file:
        reader = csv.reader(file)
        header = next(reader)  # Read the header row
        
        sorting_tasks = []
        
        for i, row in enumerate(reader):
            print(i)    
            raw_messages_string = row[header.index(MESSAGE_COL_NAME)]
            sorting_tasks.append(write_sorting_result(raw_messages_string))
        
        await asyncio.gather(*sorting_tasks)

if __name__ == '__main__':
    asyncio.run(main())