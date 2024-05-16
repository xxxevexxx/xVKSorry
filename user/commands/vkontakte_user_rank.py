from const import Const
from vkbottle import API
from user.rules import Commands
from models.usermodel import Users
from user.decorators import vkontakte_on_error
from vkbottle.user import UserLabeler, Message


labeler = UserLabeler()


@labeler.message(Commands("..", ["rank", "ранг"], 5))
@vkontakte_on_error
async def vkontakte_rank(client: API, message: Message):
    """
    :param name: Rank
    :param level: 1
    :param command: .. rank
    :param description: Установит ранг пользователю
    """
    ranks = {"1": "User", "2": "Helper", "3": "Moderator", "4": "Administrator"}
    if message.reply_message is None:
        return await client.xxx.method.edit(message, f"[Rank] {Const.WARNING} The forwarded message is missing.")
    if len(message.text.split(" ")) < 3:
        return await client.xxx.method.edit(message, f"[Rank] {Const.WARNING} Required parameter is missing.")
    if message.text.split(" ")[2] not in ranks:
        return await client.xxx.method.edit(message, f"[Rank] {Const.WARNING} Incorrect rank was passed.")
    rank = int(message.text.split(" ")[2])
    if not await Users.filter(user=message.reply_message.from_id).first():
        return await client.xxx.method.edit(message, f"[Rank] {Const.WARNING} This user is not registered.")
    await client.xxx.user.set_rank(message.reply_message.from_id, rank)
    return await client.xxx.method.edit(
        message, f"[Rank] {Const.YES} [id{message.reply_message.from_id}|User rank set to {ranks[str(rank)]}]"
    )