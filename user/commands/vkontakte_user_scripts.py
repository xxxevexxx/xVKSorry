from const import Const

from vkbottle import API
from user.rules import Commands
from user.decorators import vkontakte_on_error
from vkbottle.user import UserLabeler, Message


labeler = UserLabeler()


@labeler.message(Commands(",,", ["li", "лайк", "автолайк"], 1))
@vkontakte_on_error
async def vkontakte_script_li(client: API, message: Message):
    if client.xxx.script.get_condition("li"):
        await client.xxx.script.set_condition("li", False)
        return await client.xxx.method.edit(message, "Автолайк выключен.")
    else:
        await client.xxx.script.set_condition("li", True)
        return await client.xxx.method.edit(message, "Автолайк включен.")


@labeler.message(Commands(",,", ["dr", "друзья", "автодрузья"], 1))
@vkontakte_on_error
async def vkontakte_script_dr(client: API, message: Message):
    if client.xxx.script.get_condition("dr"):
        await client.xxx.script.set_condition("dr", False)
        return await client.xxx.method.edit(message, "Автодрузья выключен.")
    else:
        await client.xxx.script.set_condition("dr", True)
        return await client.xxx.method.edit(message, "Автодрузья включен.")


@labeler.message(Commands(",,", ["uv", "уведы", "автоуведы"], 1))
@vkontakte_on_error
async def vkontakte_script_uv(client: API, message: Message):
    if client.xxx.script.get_condition("uv"):
        await client.xxx.script.set_condition("uv", False)
        return await client.xxx.method.edit(message, "Автоуведы выключен.")
    else:
        await client.xxx.script.set_condition("uv", True)
        return await client.xxx.method.edit(message, "Автоуведы включен.")


@labeler.message(Commands(",,", ["ot", "отписка", "автоотписка"], 1))
@vkontakte_on_error
async def vkontakte_script_ot(client: API, message: Message):
    if client.xxx.script.get_condition("ot"):
        await client.xxx.script.set_condition("ot", False)
        return await client.xxx.method.edit(message, "Автоотписка выключен.")
    else:
        await client.xxx.script.set_condition("ot", True)
        return await client.xxx.method.edit(message, "Автоотписка включен.")


@labeler.message(Commands(",,", ["cl", "чистка", "авточистка"], 1))
@vkontakte_on_error
async def vkontakte_script_cl(client: API, message: Message):
    if client.xxx.script.get_condition("cl"):
        await client.xxx.script.set_condition("cl", False)
        return await client.xxx.method.edit(message, "Авточистка выключен.")
    else:
        await client.xxx.script.set_condition("cl", True)
        return await client.xxx.method.edit(message, "Авточистка включен.")


@labeler.message(Commands(",,", ["ar", "реки", "автореки"], 1))
@vkontakte_on_error
async def vkontakte_script_ar(client: API, message: Message):
    if client.xxx.script.get_condition("ar"):
        await client.xxx.script.set_condition("ar", False)
        return await client.xxx.method.edit(message, "Автореки выключен.")
    else:
        await client.xxx.script.set_condition("ar", True)
        return await client.xxx.method.edit(message, "Автореки включен.")