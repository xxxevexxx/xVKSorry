from const import Const
from vkbottle import API
from user.rules import Commands
from user.decorators import vkontakte_on_error
from vkbottle.user import UserLabeler, Message


labeler = UserLabeler()


@labeler.message(Commands("..", ["message", "сообщение"], 1))
@vkontakte_on_error
async def vkontakte_message(client: API, message: Message):
    """
    :param name: Message
    :param level: 1
    :param command: .. message
    :param description: Отправит сообщение в ЛС
    """
    if message.reply_message is None:
        return await client.xxx.method.edit(message, f"[Message] {Const.WARNING} The forwarded message is missing.")
    if len(message.text.split("\n", maxsplit=1)) < 2:
        return await client.xxx.method.edit(message, f"[Message] {Const.WARNING} You must specify the text of the message.")
    text = message.text.split("\n", maxsplit=1)[1]
    await client.xxx.method.send(message, message.reply_message.from_id, text)
    return await client.xxx.method.edit(message, f"[Message] {Const.YES} Successfully save this object.")
