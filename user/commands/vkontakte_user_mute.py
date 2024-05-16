from const import Const
from vkbottle import API
from user.rules import Commands
from user.decorators import vkontakte_on_error
from vkbottle.user import UserLabeler, Message


labeler = UserLabeler()


@labeler.message(Commands("..", ["+mute", "+мут"], 1))
@vkontakte_on_error
async def vkontakte_create_mute(client: API, message: Message):
    """
    :param name: Mute
    :param level: 1
    :param command: .. +mute
    :param description: Запретит юзеру писать
    """
    if message.reply_message is None:
        return await client.xxx.method.edit(message, f"[Mute] {Const.WARNING} There is no object for the action.")
    if message.from_id == message.reply_message.from_id:
        return await client.xxx.method.edit(message, f"[Mute] {Const.WARNING} You can't apply it on yourself.")
    await client.xxx.request(
        method="changeConversationMemberRestrictions",
        data={
            "member_ids": message.reply_message.from_id,
            "peer_id": message.peer_id,
            "action": "ro",
            "for": 3600,
        }
    )
    return await client.xxx.method.edit(message, f"[Mute] {Const.YES} Yes")


@labeler.message(Commands("..", ["-mute", "-мут"], 1))
@vkontakte_on_error
async def vkontakte_delete_mute(client: API, message: Message):
    """
    :param name: Mute
    :param level: 1
    :param command: .. -mute
    :param description: Запретит юзеру писать
    """