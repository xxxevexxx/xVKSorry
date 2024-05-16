from functools import wraps
from config import ProjectVar
from vkbottle.bot import Message


def vkontakte_on_error(func):
    @wraps(func)
    async def wrapper(message: Message):
        try:
            if ProjectVar.CHATS.get(message.from_id) == message.message_id: return
            if message.peer_id > 2000000000: ProjectVar.CHATS[message.from_id] = message.message_id
            return await func(message.ctx_api, message)
        except Exception as error:
            ...

    return wrapper
