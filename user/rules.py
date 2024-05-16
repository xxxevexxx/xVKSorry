from config import ProjectVar
from vkbottle.bot import Message, rules


class Commands(rules.ABCRule[Message]):

    def __init__(self, prefix, command, rank):
        self.prefix = prefix
        self.command = command
        self.rank = rank

    async def check(self, message: Message):
        client = message.ctx_api

        if not client.xxx.user.get_rank() >= self.rank: return False

        if message.text is None: return False
        if message.out == 0: return False

        if message.text.split(" ")[0].lower() in list(client.xxx.alias.aliases.keys()):
            alias_command = client.xxx.alias.get_alias(message.text.split(" ")[0].lower())
            message.text = message.text.replace(message.text.split(" ")[0], alias_command)

        command = message.text.split("\n")[0].split(" ")
        if len(command) < 2: return False

        accept_command_list = ["connect", "disconnect", "привязать", "отвязать"]
        if not 0 < message.peer_id < 2000000000 and command[1] not in accept_command_list:
            if message.peer_id not in client.xxx.user.get_chats_list(): return False

        if isinstance(self.prefix, str):
            self.prefix = [self.prefix]
        if ".." in self.prefix: self.prefix = ["..", client.xxx.user.get_prefix_commands()]
        if ",," in self.prefix: self.prefix = [",,", client.xxx.user.get_prefix_scripts()]

        result = bool(command[0].lower() in self.prefix and command[1].lower() in self.command)
        if result: await client.xxx.user.set_command_time()
        return result


class Trigger(rules.ABCRule[Message]):

    def __init__(self):
      ...

    async def check(self, message: Message):
        if message.text is None: return
        if message.from_id == message.ctx_api.xxx.user_id: return False
        if not 0 < message.peer_id < 2000000000:
            if message.peer_id not in message.ctx_api.xxx.user.get_chats_list():
                return
        for trigger in list(message.ctx_api.xxx.trigger.triggers.keys()):
            if message.text.lower() in message.ctx_api.xxx.trigger.triggers[trigger]["trigger"]:
                message.text = message.ctx_api.xxx.trigger.triggers[trigger]["command"]
                return True
        return False


class Trusted(rules.ABCRule[Message]):

    def __init__(self):
        ...

    async def check(self, message: Message):
        prefix = message.ctx_api.xxx.user.get_prefix_repeats()
        if message.text is None: return False
        if message.from_id not in message.ctx_api.xxx.user.get_trusted_list(): return False
        if len(message.text) <= len(prefix): return False
        return message.text[:len(prefix)] == prefix


class Ignore(rules.ABCRule[Message]):

    def __init__(self):
        ...

    async def check(self, message: Message):
        return message.from_id in message.ctx_api.xxx.user.get_ignore_list()
