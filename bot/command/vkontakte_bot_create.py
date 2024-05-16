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


class HTTPClient:

    def __init__(self, login: str, password: str):
        self.login = login
        self.password = password
        self.session = requests.Session()

    def auth(self, two_fa: bool = False, code: str = None):
        data = self.session.get(
            f"https://oauth.vk.com/token",
            params={
                "grant_type": "password",
                "client_id": "6146827",
                "client_secret": "qVxWRF1CwHERuIrKBnqe",
                "username": self.login,
                "password": self.password,
                "v": "5.130",
                "2fa_supported": "1",
                "force_sms": "1" if two_fa else "0",
                "code": code if two_fa else None,
            }
        ).json()

        return data


@labeler.message(Commands(["/"], ["create"]))
@vkontakte_on_error
async def vkontakte_create(client: API, message: Message):
    if await Users.filter(user=message.from_id).first() is not None:
        return await client.messages.send(
            peer_id=message.peer_id,
            message="You are already registered.",
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
    await Users.create(user=message.from_id, token=encrypt_data(token))
    user = UserController(message.from_id)
    ProjectVar.USERS[message.from_id] = user
    await ProjectVar.USERS[message.from_id].init()
    await client.messages.send(
        peer_id=message.peer_id,
        message=f"Success",
        random_id=0
    )


@labeler.message(Commands(["/"], ["test"]))
async def test_create(message: Message):
    user = await Users.filter(user=message.from_id).first()
    print(user.token)


# @router.message(AuthStates.password)
# async def set_password(message: Message, state: FSMContext):
#     await state.update_data(password=message.text)
#     data = await state.get_data()
#     await state.set_state(AuthStates.code)
#
#     client = HTTPClient(login=data["login"], password=data["password"])
#     response = client.auth()
#
#     if response.get("error_description", "").lower() == 'неправильный логин или пароль':
#         await state.clear()
#         await message.answer(f"{Icons.WARNING} {response.get('error_description')}")
#
#     elif response.get("captcha_sid"):
#         await state.clear()
#         await message.answer(f"{Icons.WARNING} Выполните запрос позже. На данный момент у вас капча.")
#         return
#
#     elif response.get("validation_sid"):
#         client.session.get(
#             "https://api.vk.com/method/auth.validatePhone",
#             params={"sid": response["validation_sid"], "v": "5.131"},
#         )
#
#         await message.answer(
#             f"{Icons.YES} Хорошо, я принял ваш пароль!\n"
#             f"{Icons.RIGHT} Осталось написать код, который должен сейчас прийти вам на своё устройство."
#         )
#     else:
#         await message.answer(
#             f"{Icons.YES} Всё супер. Вот ваш токен:\n"
#             f"{Icons.LIST} {response['access_token']}"
#         )
#
#
# @router.message(AuthStates.code)
# async def set_code(message: Message, state: FSMContext):
#     await state.update_data(code=message.text)
#     data = await state.get_data()
#     await state.clear()
#
#     client = HTTPClient(login=data["login"], password=data["password"])
#     response = client.auth(two_fa=True, code=data["code"])
#
#     await message.answer(
#         f"{Icons.YES} Всё супер. Вот ваш токен:\n"
#         f"{response['access_token']}"
#     )