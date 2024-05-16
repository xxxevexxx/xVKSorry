from const import Const
from vkbottle import API
from user.rules import Commands, Ignore
from user.decorators import vkontakte_on_error
from vkbottle.user import UserLabeler, Message


labeler = UserLabeler()


@labeler.message(Commands("..", ["ignores", "игнор"], 1))
@vkontakte_on_error
async def vkontakte_ignores(client: API, message: Message):
    """
    :param name: Ignore
    :param level: 5
    :param command: .. ignores
    :param description: Отобразит игнор лист
    """
    if len(client.xxx.user.get_ignore_list()) == 0:
        return await client.xxx.method.edit(message, f"[Ignore] {Const.WARNING} There is no objects in the database.")
    user_list = await client.users.get(user_ids=",".join(map(str, client.xxx.user.get_ignore_list())))
    ignores = ""
    for enum, user in enumerate(user_list):
        enum = enum + 1 if enum + 1 >= 10 else f"0{enum + 1}"
        ignores += f"{Const.LS}{enum}{Const.PS} {Const.SS} {Const.USER}[id{user.id}|{user.first_name} {user.last_name}]\n"
    return await client.xxx.method.edit(message, f"[Ignore] {Const.YES} Information about objects.\n\n{ignores}")


@labeler.message(Commands("..", ["+ignore", "+игнор"], 1))
@vkontakte_on_error
async def vkontakte_create_ignore(client: API, message: Message):
    """
    :param name: Ignore
    :param level: 5
    :param command: .. +ignore
    :param description: Добавит в игнор лист
    """
    if message.reply_message is None:
        return await client.xxx.method.edit(message, f"[Ignore] {Const.WARNING} There is no object for the action.")
    if message.from_id == message.reply_message.from_id:
        return await client.xxx.method.edit(message, f"[Ignore] {Const.WARNING} You can't apply it on yourself.")
    if message.reply_message.from_id in client.xxx.user.get_ignore_list():
        return await client.xxx.method.edit(message, f"[Ignore] {Const.WARNING} This user is already in the ignore list.")
    await client.xxx.user.set_ignore_list(message.reply_message.from_id, "+")
    return await client.xxx.method.edit(message, f"[Ignore] {Const.YES} [id{message.reply_message.from_id}|User added to the ignore list.]")


@labeler.message(Commands("..", ["-ignore", "-игнор"], 1))
@vkontakte_on_error
async def vkontakte_delete_ignore(client: API, message: Message):
    """
    :param name: Ignore
    :param level: 5
    :param command: .. -ignore
    :param description: Удалит из игнор листа
    """
    if message.reply_message is None:
        return await client.xxx.method.edit(message, f"[Ignore] {Const.WARNING} There is no object for the action.")
    if message.reply_message.from_id not in client.xxx.user.get_ignore_list():
        return await client.xxx.method.edit(message, f"[Ignore] {Const.WARNING} This user is not in the ignore list.")
    await client.xxx.user.set_ignore_list(message.reply_message.from_id, "-")
    return await client.xxx.method.edit(message, f"[Ignore] {Const.YES} [id{message.reply_message.from_id}|User delete to the ignore list.]")


@labeler.message(Ignore())
@vkontakte_on_error
async def vkontakte_ignore(client: API, message: Message):
    try: await client.messages.delete(peer_id=message.peer_id, message_ids=message.id)
    except: ...
