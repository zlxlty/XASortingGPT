from typing import Dict, List

from model import Message

"""
Segment names for different parts of the ChatGPT conversation
"""
SEG_BEGINNING = "beginning"
SEG_BASIC = "basic"
SEG_CHARACTER = "character"
SEG_INTEREST = "interest"
SEG_STORY = "story"

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

ROLE_USR = "user"
ROLE_BOT = "assistant"
ROLE_SYS = "system"
STR_QUAL_JUDGEMENT = "quality_judgement"
STR_USERNAME = "name"
STR_MESSAGES = "messages"
STR_SORTING = "house_preference"
STR_GPT_FUNC_INPUT = "gpt_function_input"
STR_GPT_FUNC_OUTPUT = "gpt_function_output"
STR_ATTRIBUTE = 'attribute'

STR_LUMA = "Luma"
STR_ACHILLECIA = "Achillecia"
STR_HEX = "Hex"
STR_NEOTRON = "Neotron"
STR_VISTAR = "Vistar"
STR_ODYSSEY = "Odyssey"

HOUSE_NAMES = [STR_LUMA, STR_ACHILLECIA, STR_HEX, STR_NEOTRON, STR_VISTAR, STR_ODYSSEY]

ATTRIBUTES_TO_HOUSE_NAMES = {
    "奋斗": STR_LUMA,
    "进取": STR_LUMA,
    "实干": STR_LUMA,
    "正义": STR_ACHILLECIA,
    "批判": STR_ACHILLECIA,
    "勇敢": STR_ACHILLECIA,
    "荣誉": STR_HEX,
    "精明": STR_HEX,
    "野心": STR_HEX,
    "严谨": STR_NEOTRON,
    "秩序": STR_NEOTRON,
    "理性": STR_NEOTRON,
    "感性": STR_VISTAR,
    "想象": STR_VISTAR,
    "自由": STR_VISTAR,
    "创新": STR_ODYSSEY,
    "突破": STR_ODYSSEY,
    "希望": STR_ODYSSEY,
}

HOUSE_NAMES_TO_ATTRIBUTES = {}
for attribute, house_name in ATTRIBUTES_TO_HOUSE_NAMES.items():
    if house_name not in HOUSE_NAMES_TO_ATTRIBUTES:
        HOUSE_NAMES_TO_ATTRIBUTES[house_name] = []
    HOUSE_NAMES_TO_ATTRIBUTES[house_name].append(attribute)
    
ATTRIBUTE_NAMES_IN_HOUSE = [",".join(attrs) for attrs in list(HOUSE_NAMES_TO_ATTRIBUTES.values())]

ATTRIBUTE_NAMES = list(ATTRIBUTES_TO_HOUSE_NAMES.keys())

PROMPT_TEMPLATE: Dict[str, List[Message]] = {
    SEG_CHARACTER: [
        Message(
            role=ROLE_USR,
            content=f"""
                我在 [] 中给你提供一段 assistant 和 user 的对话，请帮我写一段连续的段落总结对话里 user 提供的所有信息。不要用列表形式，用一段完整的段落。请直接开始总结，不要写任何开头。{{{STR_MESSAGES}}}
            """,
        )
    ],
    SEG_STORY: [
        Message(
            role=ROLE_USR,
            content=f"""
                我在 [] 中给你提供一段 assistant 和 user 的对话，对话中他们共同创作了一个故事。请帮我把这段故事生动，完整，流畅的从对话中提取出来。请直接开始故事，不要写任何开头。{{{STR_MESSAGES}}}
            """,
        )
    ],
    
    STR_QUAL_JUDGEMENT:[
        Message(
            role=ROLE_USR,
            content=f"""
            你是一个顶尖的心理侧写师，现在你需要根据 {{{STR_USERNAME}}} 提供的信息判断用户和这一组性格特质一起的契合度有多少。
            
            性格特质：{{{STR_ATTRIBUTE}}}。
            
            你知道 {{{STR_USERNAME}}} 的以下信息：
            
            {{{STR_USERNAME}}}的性格特点是这样的：{{{SEG_CHARACTER}}}
            
            {{{STR_USERNAME}}}的兴趣爱好有这些：{{{SEG_INTEREST}}}
            
            {{{STR_USERNAME}}}为了表达自己创作了这样的故事：{{{SEG_STORY}}}
            
            你需要根据{{{STR_USERNAME}}}的所有信息，为一组性格特质打一个契合度百分比，百分比越高，{{{STR_USERNAME}}}越符合这一组特质，百分比越低，越不符合这一组特质。在合理的情况下可以大胆的给小于50.2%的低分。分数必须精确到一位小数。
            在打分之后，你需要写一个完整的大约300字的报告尽可能从各个方面详细的论述你打出这个分数的理由。理由正反面都可以。
            """
        )    
    ],
    STR_GPT_FUNC_OUTPUT: [
        Message(
            role=ROLE_SYS,
            content=f"""
            You are a world class algorithm for extracting information in structured formats.
            """,
        ),
        Message(
            role=ROLE_USR,
            content=f"""
            Use the given format to extract information from the following input: {{{STR_QUAL_JUDGEMENT}}}
            """,
        ),
        Message(
            role=ROLE_USR,
            content=f"""
            Tips: Make sure to answer in the correct format
            """,
        ),
    ],
}