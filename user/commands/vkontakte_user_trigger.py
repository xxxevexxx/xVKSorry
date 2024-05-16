from const import Const
from vkbottle import API
from user.rules import Commands, Trigger
from user.decorators import vkontakte_on_error
from vkbottle.user import UserLabeler, Message


labeler = UserLabeler()


@labeler.message(Commands("..", ["triggers", "триггеры"], 1))
@vkontakte_on_error
async def vkontakte_triggers(client: API, message: Message):
    """
    :param name: Trigger
    :param level: 6
    :param command: .. triggers
    :param description: Отобразит список триггеров
    """
    if len(client.xxx.trigger.triggers) == 0:
        return await client.xxx.method.edit(message, f"[Trigger] {Const.WARNING} There is no objects in the database.")
    triggers = ""
    for enum, trigger in enumerate(client.xxx.trigger.triggers.items()):
        enum = enum + 1 if enum + 1 >= 10 else f"0{enum + 1}"
        triggers += f"{Const.LS}{enum}{Const.PS} {Const.FF} [{trigger[0]}] {Const.SS} {trigger[1]['trigger']} {Const.SS} [{trigger[1]['command']}]\n"
    return await client.xxx.method.edit(message, f"[Trigger] {Const.YES} Information about objects.\n\n{triggers}")


@labeler.message(Commands("..", ["+trigger", "+триггер"], 1))
@vkontakte_on_error
async def vkontakte_create_trigger(client: API, message: Message):
    """
    :param name: Trigger
    :param level: 6
    :param command: .. +trigger
    :param description: Создаст новый триггер
    """
    if len(message.text.split("\n")[0].split(" ")) < 3:
        return await client.xxx.method.edit(message, f"[Trigger] {Const.WARNING} You must specify a name.")
    name = message.text.split("\n")[0].split(" ")[2].lower()
    if len(name) > 10:
        return await client.xxx.method.edit(message, f"[Trigger] {Const.WARNING} Maximum length of an object name.")
    if name in list(client.xxx.trigger.triggers.keys()):
        return await client.xxx.method.edit(message, f"[Trigger] {Const.WARNING} This name is already taken.")
    if len(message.text.split("\n")) < 2:
        return await client.xxx.method.edit(message, f"[Trigger] {Const.WARNING} Specify a list of trigger words.")
    trigger = message.text.lower().split("\n")[1].split("/")
    if len(message.text.split("\n")) < 3:
        return await client.xxx.method.edit(message, f"[Trigger] {Const.WARNING} Specify the command when activating the trigger.")
    command = message.text.split("\n", maxsplit=2)[2]
    await client.xxx.trigger.set_trigger(
        dict(name=name, trigger=trigger, command=command)
    )
    return await client.xxx.method.edit(message, f"[Trigger] {Const.YES} A new object has been created.")


@labeler.message(Commands("..", ["-триггер", "-trigger"], 1))
@vkontakte_on_error
async def vkontakte_remove_trigger(client: API, message: Message):
    """
    :param name: Trigger
    :param level: 6
    :param command: .. -trigger
    :param description: Удалит имеющийся триггер
    """
    if len(message.text.split(" ")) < 3:
        return await client.xxx.method.edit(message, f"[Trigger] {Const.WARNING} You must specify a name.")
    name = message.text.split(" ")[2].lower()
    if len(name) > 10:
        return await client.xxx.method.edit(message, f"[Trigger] {Const.WARNING} Maximum length of an object name.")
    if name not in list(client.xxx.trigger.triggers.keys()):
        return await client.xxx.method.edit(message, f"[Trigger] {Const.WARNING} This name is already taken.")
    await client.xxx.trigger.del_trigger(name)
    return await client.xxx.method.edit(message, f"[Trigger] {Const.YES} An old object was deleted.")


@labeler.message(Trigger())
@vkontakte_on_error
async def vkontakte_trigger(client: API, message: Message):
    await client.messages.send(
        peer_id=message.peer_id,
        message=message.text,
        random_id=0
    )
