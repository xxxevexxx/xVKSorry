from const import Const
from vkbottle import API
from user.rules import Commands
from user.decorators import vkontakte_on_error
from vkbottle.user import UserLabeler, Message


labeler = UserLabeler()


@labeler.message(Commands("..", ["templates", "шаблоны"], 1))
@vkontakte_on_error
async def vkontakte_templates(client: API, message: Message):
    """
    :param name: Template
    :param level: 8
    :param command: .. templates
    :param description: Отобразит список шаблонов
    """
    if len(client.xxx.template.templates) == 0:
        return await client.xxx.method.edit(message, f"[Template] {Const.WARNING} There is no objects in the database.")
    templates = ""
    for enum, template in enumerate(client.xxx.template.templates.items()):
        enum = enum + 1 if enum + 1 >= 10 else f"0{enum + 1}"
        templates += f"{Const.LS}{enum}{Const.PS} {Const.FF} [{template[0]}] {Const.SS} [Template]\n"
    return await client.xxx.method.edit(message, f"[Template] {Const.YES} Information about objects.\n\n{templates}")


@labeler.message(Commands("..", ["template", "шаблон"], 1))
@vkontakte_on_error
async def vkontakte_template(client: API, message: Message):
    """
    :param name: Template
    :param level: 8
    :param command: .. template
    :param description: Вызовет имеющийся шаблон
    """
    if len(message.text.split(" ")) < 3:
        return await client.xxx.method.edit(message, f"[Template] {Const.WARNING} You must specify a name.")
    if message.text.split(" ")[2].lower() not in list(client.xxx.template.templates.keys()):
        return await client.xxx.method.edit(message, f"[Template] {Const.WARNING} This name is already taken.")
    template_object = client.xxx.template.get_template(message.text.split(" ")[2].lower())
    await client.messages.delete(
        peer_id=message.from_id, message_ids=message.id, delete_for_all="1" if message.from_id != message.peer_id else "0"
    )
    message_object = await client.messages.get_by_id(message_ids=template_object["message_id"])
    message_object = message_object.items[0]
    attachments = []
    for attachment in message_object.attachments:
        attachment_type = attachment.type.value
        attachment_object = getattr(attachment, attachment_type)
        if not hasattr(attachment_object, "id") or not hasattr(attachment_object, "owner_id"):
            continue
        attachment_string = (
            f"{attachment_type}{attachment_object.owner_id}_{attachment_object.id}"
        )
        if attachment_object.access_key:
            attachment_string += f"_{attachment_object.access_key}"
        attachments.append(attachment_string)
    return await client.messages.send(
        peer_id=message.peer_id,
        message=message_object.text,
        attachment=",".join(attachments),
        random_id=0
    )


@labeler.message(Commands("..", ["+template", "+шаблон"], 1))
@vkontakte_on_error
async def vkontakte_create_template(client: API, message: Message):
    """
    :param name: Template
    :param level: 8
    :param command: .. +template
    :param description: Создаст новый шаблон
    """
    if len(message.text.split(" ")) < 3:
        return await client.xxx.method.edit(message, f"[Template] {Const.WARNING} You must specify a name.")
    name = message.text.split(" ")[2].lower()
    if len(name) > 10:
        return await client.xxx.method.edit(message, f"[Template] {Const.WARNING} Maximum length of an object name.")
    if name in list(client.xxx.template.templates.keys()):
        return await client.xxx.method.edit(message, f"[Template] {Const.WARNING} This name is already taken.")
    if message.reply_message is None:
        return await client.xxx.method.edit(message, f"[Template] {Const.WARNING} There is no object for the action.")
    message_object = await client.messages.send(
        peer_id=message.from_id,
        message=message.reply_message.text,
        attachment=",".join(message.reply_message.get_attachment_strings()),
        random_id=0
    )
    await client.xxx.template.set_template(
        dict(name=name, message_id=message_object)
    )
    return await client.xxx.method.edit(message, f"[Template] {Const.YES} A new object has been created.")


@labeler.message(Commands("..", ["-шаблон", "-template"], 1))
@vkontakte_on_error
async def vkontakte_remove_template(client: API, message: Message):
    """
    :param name: Template
    :param level: 8
    :param command: .. -template
    :param description: Удалит имеющийся шаблон
    """
    if len(message.text.split(" ")) < 3:
        return await client.xxx.method.edit(message, f"[Template] {Const.WARNING} You must specify a name.")
    name = message.text.split(" ")[2].lower()
    if len(name) > 10:
        return await client.xxx.method.edit(message, f"[Template] {Const.WARNING} Maximum length of an object name.")
    if name not in list(client.xxx.template.templates.keys()):
        return await client.xxx.method.edit(message, f"[Template] {Const.WARNING} This name is already taken.")
    template_object = client.xxx.template.get_template(message.text.split(" ")[2].lower())
    await client.xxx.template.del_template(name)
    await client.messages.delete(
        peer_id=message.from_id, message_ids=template_object["message_id"],
        delete_for_all="1" if message.from_id != message.peer_id else "0"
    )
    return await client.xxx.method.edit(message, f"[Template] {Const.YES} An old object was deleted.")
