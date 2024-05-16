import time

from const import Const
from vkbottle import API
from user.rules import Commands
from user.decorators import vkontakte_on_error
from vkbottle.user import UserLabeler, Message


labeler = UserLabeler()


@labeler.message(Commands("..", ["+prefix", "+префикс"], 1))
@vkontakte_on_error
async def vkontakte_create_prefix(client: API, message: Message):
    """
    :param name: Prefix
    :param level: 4
    :param command: .. +prefix
    :param description: Сменит указанный префикс
    """
    if len(message.text.split(" ")) < 4:
        return await client.xxx.method.edit(message, f"[Prefix] {Const.WARNING} Required parameter is missing.")
    default_prefix = message.text.split(" ")[2]
    create_prefix = message.text.split(" ")[3]
    default_prefixes = {
        "..": client.xxx.user.set_prefix_commands,
        ",,": client.xxx.user.set_prefix_scripts,
        "#": client.xxx.user.set_prefix_repeats,
    }
    if default_prefixes.get(default_prefix) is None:
        return await client.xxx.method.edit(message, f"[Prefix] {Const.WARNING} Incorrect default prefix.")
    await default_prefixes[default_prefix](create_prefix)
    return await client.xxx.method.edit(message, f"[Prefix] {Const.YES} The prefix has been successfully changed.")


@labeler.message(Commands("..", ["-prefix", "-префикс"], 1))
@vkontakte_on_error
async def vkontakte_remove_prefix(client: API, message: Message):
    """
    :param name: Prefix
    :param level: 4
    :param command: .. -prefix
    :param description: Удалит указанный префикс
    """
    if len(message.text.split(" ")) < 3:
        return await client.xxx.method.edit(message, f"[Prefix] {Const.WARNING} Required parameter is missing.")
    default_prefix = message.text.split(" ")[2]
    default_prefixes = {
        "..": client.xxx.user.set_prefix_commands,
        ",,": client.xxx.user.set_prefix_scripts,
        "#": client.xxx.user.set_prefix_repeats,
    }
    if default_prefixes.get(default_prefix) is None:
        return await client.xxx.method.edit(message, f"[Prefix] {Const.WARNING} Incorrect default prefix.")
    await default_prefixes[default_prefix](default_prefix)
    return await client.xxx.method.edit(message, f"[Prefix] {Const.YES} The prefix has been successfully removed.")


@labeler.message(Commands("..", ["prefixes", "префиксы"], 1))
@vkontakte_on_error
async def vkontakte_prefixes(client: API, message: Message):
    """
    :param name: Prefix
    :param level: 4
    :param command: .. prefix
    :param description: Отобразит информацию префиксов
    """
    send_message = (
        f"[Prefix] {Const.SETTINGS} Prefixes:\n\n"
        f"[..] {Const.SS} Command: {client.xxx.user.get_prefix_commands()}\n"
        f"[,,] {Const.SS} Script: {client.xxx.user.get_prefix_scripts()}\n"
        f"[#] {Const.SS} Repeat: {client.xxx.user.get_prefix_repeats()}"
    )
    return await client.xxx.method.edit(message, send_message)