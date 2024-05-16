from const import Const
from vkbottle import API
from datetime import datetime
from user.rules import Commands
from user.decorators import vkontakte_on_error
from vkbottle.user import UserLabeler, Message


labeler = UserLabeler()


@labeler.message(Commands("..", ["info", "инфо"], 1))
@vkontakte_on_error
async def vkontakte_profile_info(client: API, message: Message):
    """
    :param name: Info
    :param level: 1
    :param command: .. info
    :param description: Отображает информацию о пользователе
    """
    ranks = {"1": "User", "2": "Helper", "3": "Moderator", "4": "Administrator", "5": "SystemAdmin", "6": "Developer"}
    register_time = datetime.utcfromtimestamp(client.xxx.user.register)
    register_time = register_time.strftime("%d.%m.%Y %H:%M:%S")
    send_message = (
        f"[Info] {Const.EARTH} Information about the account.\n\n"
        f"{Const.SS} NickName: {client.xxx.user.get_nick()}\n"
        f"{Const.SS} Balance: {client.xxx.user.get_balance()}\n"
        f"{Const.SS} Rank: {ranks[str(client.xxx.user.get_rank())]}\n\n"
        f"{Const.SS} Templates: {len(client.xxx.template.templates)}\n"
        f"{Const.SS} Triggers: {len(client.xxx.trigger.triggers)}\n"
        f"{Const.SS} Aliases: {len(client.xxx.alias.aliases)}\n\n"
        f"{Const.SS} Trusteds: {len(client.xxx.user.trusted_list)}\n"
        f"{Const.SS} Ignores: {len(client.xxx.user.ignore_list)}\n"
        f"{Const.SS} Chats: {len(client.xxx.user.chats_list)}\n\n"
        f"{Const.SS} Commands: {client.xxx.user.get_prefix_commands()}\n"
        f"{Const.SS} Repeats: {client.xxx.user.get_prefix_repeats()}\n"
        f"{Const.SS} Scripts: {client.xxx.user.get_prefix_scripts()}\n\n"
        f"[Info] {Const.EARTH} Register time: {register_time}.\n\n"
    )
    return await client.xxx.method.edit(message, send_message)


@labeler.message(Commands(",,", ["info", "инфо"], 1))
@vkontakte_on_error
async def vkontakte_scripts_info(client: API, message: Message):
    send_message = (
        f"[Info] {Const.EARTH} Information about the scripts.\n\n"
        f"{Const.SS} AutoLike: {'✅' if client.xxx.script.get_condition('li') else '❎'}\n"
        f"{Const.SS} AutoClear: {'✅' if client.xxx.script.get_condition('cl') else '❎'}\n"
        f"{Const.SS} AutoAccept: {'✅' if client.xxx.script.get_condition('dr') else '❎'}\n"
        f"{Const.SS} AutoNotification: {'✅' if client.xxx.script.get_condition('uv') else '❎'}\n"
        f"{Const.SS} AutoUnsubscribe: {'✅' if client.xxx.script.get_condition('ot') else '❎'}\n"
        f"{Const.SS} AutoRecomendation: {'✅' if client.xxx.script.get_condition('ar') else '❎'}\n"
    )
    return await client.xxx.method.edit(message, send_message)


@labeler.message(Commands(",,", ["stats", "стата"], 1))
@vkontakte_on_error
async def vkontakte_scripts_stats(client: API, message: Message):
    send_message = (
        f"[Info] {Const.EARTH} Statistic about the scripts.\n\n"
        f"{Const.SS} AutoLike: {client.xxx.script.get_stats('li')}\n"
        f"{Const.SS} AutoClear: {client.xxx.script.get_stats('cl')}\n"
        f"{Const.SS} AutoAccept: {client.xxx.script.get_stats('dr')}\n"
        f"{Const.SS} AutoNotification: {client.xxx.script.get_stats('uv')}\n"
        f"{Const.SS} AutoUnsubscribe: {client.xxx.script.get_stats('ot')}\n"
        f"{Const.SS} AutoRecomendation: {client.xxx.script.get_stats('ar')}\n"
    )
    return await client.xxx.method.edit(message, send_message)

