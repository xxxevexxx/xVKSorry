from const import Const
from vkbottle import API
from user.rules import Commands, Trusted
from user.decorators import vkontakte_on_error
from vkbottle.user import UserLabeler, Message


labeler = UserLabeler()


@labeler.message(Commands("..", ["trusteds", "доверенные"], 1))
@vkontakte_on_error
async def vkontakte_trusteds(client: API, message: Message):
    """
    :param name: Trusted
    :param level: 7
    :param command: .. trusteds
    :param description: Отобразит лист доверенных
    """
    if len(client.xxx.user.get_trusted_list()) == 0:
        return await client.xxx.method.edit(message, f"[Trusted] {Const.WARNING} There is no objects in the database.")
    user_list = await client.users.get(user_ids=",".join(map(str, client.xxx.user.get_trusted_list())))
    trusteds = ""
    for enum, user in enumerate(user_list):
        enum = enum + 1 if enum + 1 >= 10 else f"0{enum + 1}"
        trusteds += f"{Const.LS}{enum}{Const.PS} {Const.SS} {Const.USER}[id{user.id}|{user.first_name} {user.last_name}]\n"
    return await client.xxx.method.edit(message, f"[Trusted] {Const.YES} Information about objects.\n\n{trusteds}")


@labeler.message(Commands("..", ["+trusted", "+доверенный"], 1))
@vkontakte_on_error
async def vkontakte_create_trusted(client: API, message: Message):
    """
    :param name: Trusted
    :param level: 7
    :param command: .. +trusted
    :param description: Добавит в лист доверенных
    """
    if message.reply_message is None:
        return await client.xxx.method.edit(message, f"[Trusted] {Const.WARNING} There is no object for the action.")
    if message.from_id == message.reply_message.from_id:
        return await client.xxx.method.edit(message, f"[Trusted] {Const.WARNING} You can't apply it on yourself.")
    if message.reply_message.from_id in client.xxx.user.get_trusted_list():
        return await client.xxx.method.edit(message, f"[Trusted] {Const.WARNING} This user is already in the trusted list.")
    await client.xxx.user.set_trusted_list(message.reply_message.from_id, "+")
    return await client.xxx.method.edit(message, f"[Trusted] {Const.YES} [id{message.reply_message.from_id}|User added to the trusted list.]")


@labeler.message(Commands("..", ["-trusted", "-доверенный"], 1))
@vkontakte_on_error
async def vkontakte_delete_trusted(client: API, message: Message):
    """
    :param name: Trusted
    :param level: 7
    :param command: .. -trusted
    :param description: Отобразит лист доверенных
    """
    if message.reply_message is None:
        return await client.xxx.method.edit(message, f"[Trusted] {Const.WARNING} There is no object for the action.")
    if message.reply_message.from_id not in client.xxx.user.get_trusted_list():
        return await client.xxx.method.edit(message, f"[Trusted] {Const.WARNING} This user is not in the trusted list.")
    await client.xxx.user.set_trusted_list(message.reply_message.from_id, "-")
    return await client.xxx.method.edit(message, f"[Trusted] {Const.YES} [id{message.reply_message.from_id}|User delete to the trusted list.]")


@labeler.message(Trusted())
@vkontakte_on_error
async def vkontakte_trusted(client: API, message: Message):
    try: return await client.messages.send(
        peer_id=message.peer_id,
        message=message.text[len(client.xxx.user.get_prefix_repeats()):],
        random_id=0
    )
    except: ...


