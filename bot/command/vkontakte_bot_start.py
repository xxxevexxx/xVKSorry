from vkbottle import API
from config import ProjectVar
from bot.rules import Commands
from vkbottle.bot import BotLabeler, Message
from bot.decorators import vkontakte_on_error


labeler = BotLabeler()


@labeler.message(Commands(["/"], ["start"]))
@vkontakte_on_error
async def vkontakte_start(client: API, message: Message):
    if ProjectVar.USERS.get(message.from_id):
        ProjectVar.USERS[message.from_id].start()
        return await client.messages.send(
            peer_id=message.peer_id,
            message=f"The /start command has been sent.",
            random_id=0
        )
    else:
        return await client.messages.send(
            peer_id=message.peer_id,
            message="You are not registered.",
            random_id=0
        )