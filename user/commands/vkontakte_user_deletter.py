import asyncio

from const import Const
from vkbottle import API
from user.rules import Commands
from user.decorators import vkontakte_on_error
from vkbottle.user import UserLabeler, Message


labeler = UserLabeler()


@labeler.message(Commands("..", ["deletter", "дд"], 1))
@vkontakte_on_error
async def vkontakte_deletter(client: API, message: Message):
    """
    :param name: Deletter
    :param level: 1
    :param command: .. deletter
    :param description: Удалит последние 3 сообщения
    """
    enumerates = 0
    if len(message.text.split(" ")) < 3: value = 4
    else: value = int(message.text.split(" ")[2]) + 1
    if value > 30:
        return await client.xxx.method.edit(message, f"[Deleter] {Const.WARNING} Message limit exceeded.")

    history = await client.messages.get_history(peer_id=message.peer_id, count=200)
    for items in history.items:
        if items.from_id == message.from_id:
            await client.messages.delete(
                peer_id=message.peer_id, message_ids=items.id,
                delete_for_all="1" if message.from_id != message.peer_id else "0"
            )
            await asyncio.sleep(0.3)
            enumerates += 1
        if enumerates == value:
            break


@labeler.message(Commands("..", ["rdeletter", "рдд"], 1))
@vkontakte_on_error
async def vkontakte_rdeletter(client: API, message: Message):
    """
    :param name: RDeletter
    :param level: 1
    :param command: .. rdeletter
    :param description: Редактирует и удалит последние 3 сообщения
    """
    enumerates = 0
    if len(message.text.split(" ")) < 3:
        value = 4
    else:
        try: value = int(message.text.split(" ")[2]) + 1
        except: value = 4
    if value > 30:
        return await client.xxx.method.edit(message, f"[RDeleter] {Const.WARNING} Message limit exceeded.")
    if len(message.text.split(" ")) < 4:
        text = f"{Const.WARNING}" * 3
    else:
        text = "".join(message.text.split(" ", maxsplit=3)[3])
    history = await client.messages.get_history(peer_id=message.peer_id, count=200)
    for items in history.items:
        if items.from_id == message.from_id:
            try: await client.messages.edit(peer_id=message.peer_id, message_id=items.id, message=text)
            except: pass
            await asyncio.sleep(0.3)
            await client.messages.delete(
                peer_id=message.peer_id, message_ids=items.id,
                delete_for_all="1" if message.from_id != message.peer_id else "0"
            )
            enumerates += 1
        if enumerates == value:
            break
