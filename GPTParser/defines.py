from typing import Dict
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
from textwrap import dedent

ROLE_USR = 'user'
ROLE_BOT = 'assistant'
ROLE_SYS = 'system'

SORTING_HAT  = 'sorting'
NAME = 'name'
MESSAGES = 'messages'

PROMPT_TEMPLATE: Dict[str, Message] = {
    SEG_CHARACTER: Message(
        role=ROLE_USR, 
        content=dedent(f'''
            我在 [] 中给你提供一段 assistant 和 user 的对话，请帮我写一段连续的段落总结对话里 user 提供的所有信息。不要用列表形式，用一段完整的段落。请直接开始总结，不要写任何开头。{{{MESSAGES}}}
        ''').strip('/n')
    ),
    
    SEG_STORY: Message(
        role=ROLE_USR,
        content=dedent(f'''
            我在 [] 中给你提供一段 assistant 和 user 的对话，对话中他们共同创作了一个故事。请帮我把这段故事生动，完整，流畅的从对话中提取出来。请直接开始故事，不要写任何开头。{{{MESSAGES}}}
        ''').strip('/n')
    ),
    
    SORTING_HAT: Message(
        role=ROLE_SYS,
        content=dedent(f'''
        假设现在你是一个设定在未来的叫X Academy的学校里的智能AI分院系统。你的职责是把新用户分到 X Academy 中六个风格迥异的学院中。这六个学院的名字和特质如下：

        学院名称：Luma, 特质: 奋斗，进取，实干；
        学院名称：Achicia, 特质: 正义，批判，勇敢；
        学院名称：Hex, 特质: 荣誉，精明，野心；
        学院名称：Neotron, 特质: 严谨，秩序，理性；
        学院名称：Vistar, 特质: 感性，想象，自由；
        学院名称：Odyssey, 特质: 创新，突破，希望。

        现在有一名叫 {{{NAME}}} 的新用户需要被你分配进一个最合适的学院。你知道 {{{NAME}}}的以下信息
        
        {{{NAME}}}的性格特点是这样的：{{{SEG_CHARACTER}}}
        
        {{{NAME}}}的兴趣爱好有这些：{{{SEG_INTEREST}}}
        
        {{{NAME}}}为了表达自己创作了这样的故事：{{{SEG_STORY}}}

        你需要只根据{{{NAME}}}的所有信息，和每个学院的特质，决定{{{NAME}}}应该被分配到哪个学院当中。记住，分院只根据每一个学院的三个关键词，不要联想其他的特质。
        并且在做出决定后，你需要从{{{NAME}}}的性格特点，兴趣爱好，和创作的故事这三个方面长篇的论述为什么{{{NAME}}}合适你选择的学院，以及从这三个方面长篇的论述为什么{{{NAME}}}不合适其他学院。
        ''').strip('/n')
    )
}

'''

'''
