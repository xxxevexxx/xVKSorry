from vkbottle import API
from config import ProjectVar
from bot.rules import Commands
from vkbottle.bot import BotLabeler, Message
from bot.decorators import vkontakte_on_error


labeler = BotLabeler()


@labeler.message(Commands(["/"], ["restart"]))
@vkontakte_on_error
async def vkontakte_restart(client: API, message: Message):
    if ProjectVar.USERS.get(message.from_id):
        await ProjectVar.USERS[message.from_id].restart()
        return await client.messages.send(
            peer_id=message.peer_id,
            message=f"The /restart command has been sent.",
            random_id=0
        )
    else:
        return await client.messages.send(
            peer_id=message.peer_id,
            message="You are not registered.",
            random_id=0
        )

