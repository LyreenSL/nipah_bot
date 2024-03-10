import re
from aiogram.filters import BaseFilter
from aiogram.types import Message
from typing import Dict, Any

from cash import TRIGGERS, ACTIONS


class WordsFilter(BaseFilter):
    def __init__(self, words: set[str]):
        self.words = words

    async def __call__(self, message: Message) -> bool:
        if not message.text:
            return False

        for word in self.words:
            if re.search(fr'(^|\W){word}($|\W)', message.text.lower(), re.IGNORECASE):
                return True
        return False


class DBWordsFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool | Dict[str, Any]:
        if not message.text:
            return False

        for item in TRIGGERS:
            if (
                message.chat.id == item['chat_id'] and
                re.search(fr"(^|\W){item['word']}($|\W)", message.text.lower(), re.IGNORECASE)
            ):
                return {'trigger_answer': item['answer']}
        return False


class DBActionsFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool | Dict[str, Any]:
        if message.sticker:
            for item in ACTIONS:
                if (
                        message.chat.id == item['chat_id'] and
                        message.sticker.file_unique_id == item['command']
                ):
                    return {'action_text': item['text'],
                            'action_interaction': item['interaction'],
                            'action_add_text': ''}
            return False

        if message.text:
            for item in ACTIONS:
                if (
                        message.chat.id == item['chat_id'] and
                        message.text.lower().startswith(item['command'])
                ):
                    return {'action_text': item['text'],
                            'action_interaction': item['interaction'],
                            'action_add_text': message.text[len(item['command']):]}
            return False

        return False
