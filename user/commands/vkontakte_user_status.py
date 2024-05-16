from const import Const
from vkbottle import API
from config import ProjectVar
from user.rules import Commands
from models.botmodel import Bots
from models.usermodel import Users
from datetime import datetime, timedelta
from user.decorators import vkontakte_on_error
from vkbottle.user import UserLabeler, Message


labeler = UserLabeler()


@labeler.message(Commands("..", ["status", "статус"], 1))
@vkontakte_on_error
async def vkontakte_status(client: API, message: Message):
    """
    :param name: Status
    :param level: 1
    :param command: .. status
    :param description: Отобразит информацию о боте
    """
    total_bot = len(await Bots.all())
    active_bot = len(ProjectVar.BOTS)
    total_user = len(await Users.all())
    active_user = len(ProjectVar.USERS)
    uptime = datetime.now() - ProjectVar.UPTIME
    uptime = "{:02}h {:02}m {:02}s".format(
        uptime.seconds // 3600,
        (uptime.seconds // 60) % 60,
        uptime.seconds % 60
    )
    datetimenow = datetime.now()
    next_six_am = datetime(datetimenow.year, datetimenow.month, datetimenow.day, 6, 0)
    if datetimenow >= next_six_am: next_six_am += timedelta(days=1)
    restart = next_six_am - datetimenow
    restart = "{:02}h {:02}m {:02}s".format(
        restart.seconds // 3600,
        (restart.seconds // 60) % 60,
        restart.seconds % 60
    )
    send_message = (
        f"[Status] {Const.EARTH} Information about the bot\n\n"
        f"{Const.SS} Total Bots: {total_bot}\n"
        f"{Const.SS} Active Bots: {active_bot}\n\n"
        f"{Const.SS} Total Users: {total_user}\n"
        f"{Const.SS} Active Users: {active_user}\n\n"
        f"{Const.SS} Uptime: {uptime}\n"
        f"{Const.SS} Restart: {restart}"
    )
    return await client.xxx.method.edit(message, send_message)
