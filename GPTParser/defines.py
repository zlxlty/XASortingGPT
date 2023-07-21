from typing import Dict, List
from model import Message

"""
Segment names for different parts of the ChatGPT conversation
"""
SEG_BEGINNING = 'beginning'
SEG_BASIC = 'basic'
SEG_CHARACTER = 'character'
SEG_INTEREST = 'interest'
SEG_STORY = 'story'

"""
Segment range for different parts of the ChatGPT conversation
"""
MESSAGE_SEGMENT = {
    SEG_BEGINNING: [0, 1],
    SEG_BASIC: [2, 5],
    SEG_CHARACTER: [6, 33],
    SEG_INTEREST: [34, 49],
    SEG_STORY: [50, 63],
}

"""
Prompts for different LLM Chains
"""

ROLE_USR = 'user'
ROLE_BOT = 'assistant'
ROLE_SYS = 'system'

STR_QUAL_JUDGEMENT  = 'quality_judgement'
STR_USERNAME = 'name'
STR_MESSAGES = 'messages'
STR_GPT_FUNC_INPUT = 'gpt_function_input'
STR_GPT_FUNC_OUTPUT = 'gpt_function_output'
ATTRIBUTE_NAMES = ["奋斗","进取","实干","正义","批判","勇敢","荣誉","精明","野心","严谨","秩序","理性","感性","想象","自由","创新","突破","希望"]

PROMPT_TEMPLATE: Dict[str, List[Message]] = {
    SEG_CHARACTER: [
        Message(
            role=ROLE_USR, 
            content=f'''
                我在 [] 中给你提供一段 assistant 和 user 的对话，请帮我写一段连续的段落总结对话里 user 提供的所有信息。不要用列表形式，用一段完整的段落。请直接开始总结，不要写任何开头。{{{STR_MESSAGES}}}
            '''
        )
    ],
    
    SEG_STORY: [
        Message(
            role=ROLE_USR,
            content=f'''
                我在 [] 中给你提供一段 assistant 和 user 的对话，对话中他们共同创作了一个故事。请帮我把这段故事生动，完整，流畅的从对话中提取出来。请直接开始故事，不要写任何开头。{{{STR_MESSAGES}}}
            '''
        )
    ],
    
    STR_QUAL_JUDGEMENT: [
        Message(
        role=ROLE_USR,
        content=f'''
            现在你是一个用户特质分析师，你需要根据用户提供的所有信息判断用户分别跟以下18个关键词的契合度有多少：
            
            关键词： {"，".join(ATTRIBUTE_NAMES)}。

            现在有一名叫 {{{STR_USERNAME}}} 的新用户需要你的特质分析。你知道 {{{STR_USERNAME}}}的以下信息
            
            {{{STR_USERNAME}}}的性格特点是这样的：{{{SEG_CHARACTER}}}
            
            {{{STR_USERNAME}}}的兴趣爱好有这些：{{{SEG_INTEREST}}}
            
            {{{STR_USERNAME}}}为了表达自己创作了这样的故事：{{{SEG_STORY}}}

            你需要根据{{{STR_USERNAME}}}的所有信息，为每一个特质打不同的一个百分比，百分比越高，{{{STR_USERNAME}}}越符合这个特质。你需要为每一个特质打分，不要跳过任何一个特质。
            记住，打给每一个特质的分数必须不同。在每一次打分之后，你需要至少从三个方面详细的论述你打出每个分数的理由。你为每个特质提供的理由必须包括用户性格特点、兴趣爱好、创作的故事这三个方面的信息。
            
            以下是两个特质打分的例子你可以参考：
            “
            2. 进取 (87%)
            理由：
            - 用户追求成就和喜欢挑战自己，这表明他有进取心。
            - 用户喜欢参加数学竞赛和解决问题，这需要进取心和积极性。
            - 用户创作的故事中，无决定以行动示范的方式引领人类社会朝着和平与协作的方向发展，这需要进取心和积极性。
            
            13. 感性 (22%)
            理由：
            - 用户火冒三丈，内心期望有机会狠狠地回应，这表明他具有一定的感性。
            - 用户的其他信息中没有明确提到感性的特点。
            - 用户创作的故事中，无决定与被操控的人们联手，发起一场彻底改革的革命，这可能体现了一定的感性。
            ”
            
            记住，给每一个特质的打分必须不同，要为全部18个特质打分并说明理由！
            '''
        )
    ],
    
    STR_GPT_FUNC_OUTPUT: [
        Message(
        role=ROLE_SYS,
        content=f'''
            You are a world class algorithm for extracting information in structured formats.
            '''
        ),
        Message(
        role=ROLE_USR,
        content=f'''
            Use the given format to extract information from the following input: {{{STR_QUAL_JUDGEMENT}}}
            '''
        ),
        Message(
        role=ROLE_USR,
        content=f'''
            Tips: Make sure to answer in the correct format
            '''
        ),
    ]
}

'''

'''
