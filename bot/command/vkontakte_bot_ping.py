import time
from const import Const
from vkbottle import API
from vkbottle.bot import Bot
from models.usermodel import Users
from vkbottle.bot import BotLabeler, Message
from bot.decorators import vkontakte_on_error
from vkbottle.dispatch.rules.base import CommandRule


labeler = BotLabeler()


@labeler.message(CommandRule("ping", ["/"]))
@vkontakte_on_error
async def vkontakte_ping(client: API, message: Message):
    times = str(float("{:.2f}".format(message.date - time.time()))).replace("-", "")
    return await client.messages.send(
        peer_id=message.peer_id,
        message=f"{Const.EARTH} PingTime: {times}sec.",
        random_id=0
    )
