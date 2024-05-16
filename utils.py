import base64
import aiohttp

from models.usermodel import Users
from fastapi import Request, HTTPException, WebSocket
from config import ProjectConfig, ProjectVar

from aiohttp import ClientSession
from vkbottle.modules import json as json_module
from typing import Optional, Any


# Кодирование данных
def encrypt_data(data):
    try:
        encrypted_data = base64.b64encode(ProjectConfig.FERNET_TOKEN.encrypt(data.encode())).decode('utf-8')
    except:
        encrypted_data = "e-e-e-e-e-e"
    return encrypted_data


# Декодирование данных
def decrypt_data(encrypted_data):
    try:
        decrypted_data = ProjectConfig.FERNET_TOKEN.decrypt(base64.b64decode(encrypted_data.encode('utf-8'))).decode()
    except:
        decrypted_data = "d-d-d-d-d-d"
    return decrypted_data


# Проверка токена
async def check_api(api):
    try:
        await api.users.get()
    except:
        return False
    else:
        return True