from const import Const
from vkbottle import API
from user.rules import Commands
from user.decorators import vkontakte_on_error
from vkbottle.user import UserLabeler, Message


labeler = UserLabeler()


@labeler.message(Commands("..", ["connect", "привязать"], 1))
@vkontakte_on_error
async def vkontakte_connect(client: API, message: Message):
    """
    :param name: Chats
    :param level: 2
    :param command: .. connect
    :param description: Привяжет бота к чату
    """
    if message.peer_id in client.xxx.user.get_chats_list():
        return await client.xxx.method.edit(message, f"[Chats] {Const.WARNING} This chat is already linked.")
    await client.xxx.user.set_chats_list(message.peer_id, "+")
    return await client.xxx.method.edit(message, f"[Chats] {Const.YES} The chat has been successfully linked.")


@labeler.message(Commands("..", ["disconnect", "отвязать"], 1))
@vkontakte_on_error
async def vkontakte_disconnect(client: API, message: Message):
    """
    :param name: Chats
    :param level: 2
    :param command: .. disconnect
    :param description: Отвяжет бота от чата
    """
    if message.peer_id not in client.xxx.user.get_chats_list():
        return await client.xxx.method.edit(message, f"[Chats] {Const.WARNING} This chat is not linked.")
    await client.xxx.user.set_chats_list(message.peer_id, "-")
    return await client.xxx.method.edit(message, f"[Chats] {Const.YES} The chat was successfully disabled.")


@labeler.message(Commands("..", ["clear", "очистить"], 1))
@vkontakte_on_error
async def vkontakte_clear(client: API, message: Message):
    """
    :param name: Chats
    :param level: 2
    :param command: .. clear
    :param description: Очистит список привязанных чатов
    """
    if len(client.xxx.user.get_chats_list()) == 0:
        return await client.xxx.method.edit(message, f"[Chats] {Const.WARNING} There are no linked chats.")
    for chat_id in list(client.xxx.user.get_chats_list()):
        await client.xxx.user.set_chats_list(chat_id, "-")
    return await client.xxx.method.edit(message, f"[Chats] {Const.YES} The list of linked chats has been cleared.")
