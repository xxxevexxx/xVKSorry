import asyncio

from const import Const
from vkbottle import API
from user.rules import Commands
from user.decorators import vkontakte_on_error
from vkbottle.user import UserLabeler, Message


labeler = UserLabeler()


@labeler.message(Commands("..", ["push", "пуши"], 1))
@vkontakte_on_error
async def vkontakte_push(client: API, message: Message):
    """
    :param name: Push
    :param level: 1
    :param command: .. push
    :param description: Отобразит 3 упомянания
    """

    await client.xxx.method.edit(message, f"[Push] {Const.LOADING} Search for messages with mentions.")
    result = await client.messages.search(peer_id=message.peer_id, q=f"id{client.xxx.user_id}", count=3, extended=0)
    for item in result.items:
        try:
            await client.messages.send(
                peer_id=item.peer_id,
                reply_to=item.id,
                message="⤴️",
                random_id=0
            )
        except: ...
        await asyncio.sleep(0.5)
    if result.items:
        return await client.xxx.method.edit(message, f"[Push] {Const.YES} Information about messages.")
    else:
        return await client.xxx.method.edit(message, f"[Push] {Const.YES} No messages found mentioning.")
