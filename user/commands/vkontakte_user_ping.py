import time

from const import Const
from vkbottle import API
from user.rules import Commands
from user.decorators import vkontakte_on_error
from vkbottle.user import UserLabeler, Message


labeler = UserLabeler()


@labeler.message(Commands("..", ["ping", "пинг"], 1))
@vkontakte_on_error
async def vkontakte_ping(client: API, message: Message):
    """
    :param name: Ping
    :param level: 1
    :param command: .. ping
    :param description: Отобразит время задержки
    """
    times = str(float("{:.2f}".format(message.date - time.time()))).replace("-", "")
    return await client.xxx.method.edit(message, f"[Ping] {Const.EARTH} PingTime {times} sec.")
