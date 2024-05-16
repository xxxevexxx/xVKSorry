from const import Const
from vkbottle import API
from user.rules import Commands
from collections import OrderedDict
from user.decorators import vkontakte_on_error
from vkbottle.user import UserLabeler, Message


labeler = UserLabeler()


@labeler.message(Commands("..", ["commands", "команды"], 1))
@vkontakte_on_error
async def vkontakte_commands(client: API, message: Message):
    """
    :param name: Command
    :param level: 1
    :param command: .. commands
    :param description: Отобразит список команд
    """
    module = {}
    command = ""
    for items in client.xxx.commands:
        if module.get(items['level']):
            module[items['level']].append(items)
        else:
            module[items['level']] = [items]

    module = OrderedDict(sorted(module.items(), key=lambda x: int(x[0])))
    for items in list(module.keys()):
        module[items] = sorted(module[items], key=lambda x: len(x['name']))

    for enum, items in enumerate((module.keys())):
        if enum == 0: command += f"— Main:\n"
        else: command += f"— {module[items][0]['name']}:\n"
        for item in module[items]:
            command += f"- {Const.LS}{item['name']}{Const.PS} {Const.SS} {item['command']} | {item['description']}\n"
        command += "\n"
    return await client.xxx.method.edit(message, command)
