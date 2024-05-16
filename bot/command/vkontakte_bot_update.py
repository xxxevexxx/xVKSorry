from vkbottle import API
from config import ProjectVar
from bot.rules import Commands
from utils import encrypt_data
from vkbottle import VKAPIError
from models.usermodel import Users
from user.controller import UserController
from vkbottle.bot import BotLabeler, Message
from bot.decorators import vkontakte_on_error


labeler = BotLabeler()


@labeler.message(Commands(["/"], ["update"]))
@vkontakte_on_error
async def vkontakte_create(client: API, message: Message):
    if await Users.filter(user=str(message.from_id)).first() is None:
        return await client.messages.send(
            peer_id=message.peer_id,
            message="You are not registered.",
            random_id=0
        )
    token = message.text.split(" ")[1]
    try:
        api = API(token)
        response = await api.users.get()
    except VKAPIError[5] as error:
        return await client.messages.send(
            peer_id=message.peer_id,
            message=f"{error}",
            random_id=0
        )
    if response[0].id != message.from_id:
        return await client.messages.send(
            peer_id=message.peer_id,
            message=f"You can only register your account.",
            random_id=0
        )
    await Users.filter(user=message.from_id).update(token=encrypt_data(token))
    user = UserController(message.from_id)
    if ProjectVar.USERS.get(message.from_id):
        ProjectVar.USERS[message.from_id].stop()
    ProjectVar.USERS[message.from_id] = user
    await ProjectVar.USERS[message.from_id].init()
    await client.messages.send(
        peer_id=message.peer_id,
        message=f"Success",
        random_id=0
    )