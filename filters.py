import re
from aiogram.filters import BaseFilter
from aiogram.types import Message
from typing import Dict, Any

from database.requests import db_get_triggers


class WordsFilter(BaseFilter):
    def __init__(self, words: set[str]):
        self.words = words

    async def __call__(self, message: Message) -> bool:
        for word in self.words:
            if message.text and re.search(fr'(^|\W){word}($|\W)', message.text.lower(), re.IGNORECASE):
                return True
        return False


class DBWordsFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool | Dict[str, Any]:
        triggers_pair = await db_get_triggers(message.chat.id)
        for pair in triggers_pair:
            if message.text and re.search(fr'(^|\W){pair[0]}($|\W)', message.text.lower(), re.IGNORECASE):
                return {'trigger_answer': pair[1]}
        return False
