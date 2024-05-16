from const import Const
from vkbottle import API
from user.rules import Commands
from user.decorators import vkontakte_on_error
from vkbottle.user import UserLabeler, Message


labeler = UserLabeler()


@labeler.message(Commands("..", ["save", "сохранить"], 1))
@vkontakte_on_error
async def vkontakte_save(client: API, message: Message):
    """
    :param name: Saver
    :param level: 1
    :param command: .. save
    :param description: Сохранит сообщение в избранное
    """
    if message.reply_message is None:
        return await client.xxx.method.edit(message, f"[Saver] {Const.WARNING} The forwarded message is missing.")
    await client.messages.send(
        peer_id=message.from_id,
        attachment=",".join(message.reply_message.get_attachment_strings()),
        message=message.reply_message.text,
        random_id=0
    )
    return await client.xxx.method.edit(message, f"[Saver] {Const.YES} Successfully save this object.")
