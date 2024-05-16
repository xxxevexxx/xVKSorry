import jwt
import aiohttp

from utils import encrypt_data
from models.usermodel import Users, Scripts
from fastapi import APIRouter, Request
from user.controller import UserController
from config import ProjectConfig, ProjectVar


router = APIRouter()


VK_URL = f"https://oauth.vk.com/token"


async def vk_number(token, data):
    ProjectVar.VK_AUTH[token] = {
        "grant_type": "password",
        "client_id": "2274003",
        "client_secret": "hHbZxrka2uZ6jB1inYsH",
        "username": data,
        "password": None,
        "v": "5.130",
        "2fa_supported": "1",
        "force_sms": "0",
    }
    return dict(status=True, description=f"Введите пароль авторизации")


async def vk_password(owner_id, data):
    ProjectVar.VK_AUTH[owner_id]["password"] = data
    async with aiohttp.ClientSession() as session:
        async with session.get(VK_URL, params=ProjectVar.VK_AUTH[owner_id]) as response:
            response = await response.json()
    if response.get("error_description", "").lower() == 'неправильный логин или пароль':
        return dict(status=False, description=f"Не правильный логин или пароль")
    if response.get("captcha_sid"):
        return dict(status=False, description=f"Капча, повтори попытку позже")
    if response.get("validation_sid"):
        SID_URL = "https://api.vk.com/method/auth.validatePhone"
        async with aiohttp.ClientSession() as session:
            async with session.get(SID_URL, params={"sid": response["validation_sid"], "v": "5.131"}) as response: ...
        return dict(status=True, description=f"Введите код авторизации")
    if response.get("access_token"):
        return await vk_token(owner_id, response["user_id"], response["access_token"])


async def vk_code(owner_id, data):
    ProjectVar.VK_AUTH[owner_id]["force_sms"] = "1"
    ProjectVar.VK_AUTH[owner_id]["code"] = data
    async with aiohttp.ClientSession() as session:
        async with session.get(VK_URL, params=ProjectVar.VK_AUTH[owner_id]) as response:
            response = await response.json()
    return await vk_token(owner_id, response["user_id"], response["access_token"])


async def vk_token(owner_id, user_id, user_token):
    user = await Users.filter(user=user_id).first()
    if user:
        if user.owner != owner_id: return dict(status=False, description=f"Аккаунт пренадлежит другому пользователю")
        await Users.filter(user=user_id).update(token=encrypt_data(user_token))
        if ProjectVar.USERS.get(user_id): ProjectVar.USERS[user_id].stop()
    else:
        user = await Users.create(user=user_id, owner=owner_id, token=encrypt_data(user_token))
        print(user.id)
        await Scripts.create(user=user)
    user = UserController(user_id)
    ProjectVar.USERS[user_id] = user
    await ProjectVar.USERS[user_id].init()
    return dict(status=True, description=f"Приятного пользования")


@router.post("/auth")
async def views_vksorry_auth(request: Request):
    data = await request.json()
    owner_id = data.get("owner_id")
    action = data.get("action")
    data = data.get("data")
    if action == "vk_number":
        return await vk_number(owner_id, data)
    if action == "vk_password":
        return await vk_password(owner_id, data)
    if action == "vk_code":
        return await vk_code(owner_id, data)

