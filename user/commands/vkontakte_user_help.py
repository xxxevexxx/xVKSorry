from const import Const
from vkbottle import API
from user.rules import Commands
from user.decorators import vkontakte_on_error
from vkbottle.user import UserLabeler, Message


labeler = UserLabeler()


@labeler.message(Commands("..", ["help", "помощь"], 1))
@vkontakte_on_error
async def vkontakte_help(client: API, message: Message):
    """
    :param name: Help
    :param level: 1
    :param command: .. help
    :param description: Отобразит полезную информацию
    """
    send_message = (
        f"[Help] {Const.EARTH} Information about for helps\n\n"
        f"{Const.SS} Telegram chat: https://xxxevexxx.ru/tgsorry/chat\n"
        f"{Const.SS} Telegram bot: https://xxxevexxx.ru/tgsorry/bot\n\n"
        f"{Const.SS} Vkontakte chat: https://xxxevexxx.ru/vksorry/chat\n"
        f"{Const.SS} Vkontakte bot: https://xxxevexxx.ru/vksorry/bot\n\n"
        f"{Const.SS} SystemAdmin: https://xxxevexxx.ru/999\n"
        f"{Const.SS} Developer: https://xxxevexxx.ru/666\n"
        f"{Const.SS} Admin: https://xxxevexxx.ru/333\n\n"
    )
    return await client.xxx.method.edit(message, send_message)