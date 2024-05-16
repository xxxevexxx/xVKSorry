from config import ProjectVar
from vkbottle.bot import Message, rules
from typing import Dict, List, Optional, Tuple, Union


class Commands(rules.ABCRule[Message]):

    def __init__(self, prefix, command):
        self.prefix = prefix
        self.command = command

    async def check(self, message: Message):
        if message.text is None: return False
        if isinstance(self.prefix, str): self.prefix = [self.prefix]
        if isinstance(self.command, str): self.command = [self.command]
        for prefix in self.prefix:
            if not message.text.startswith(prefix): continue
            for cmd in self.command:
                if not message.text[len(prefix):].startswith(cmd): continue
                return True
        return False


class FromUserRule(rules.ABCRule[Message]):

    def __init__(self, from_user: bool = True):
        self.from_user = from_user

    async def check(self, message: Message) -> bool:
        return self.from_user is (message.from_id > 0)
