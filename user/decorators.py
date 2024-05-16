import asyncio

from loguru import logger
from functools import wraps
from vkbottle import VKAPIError


def vkontakte_on_error(func):
    @wraps(func)
    async def wrapper(message):
        try:
            return await func(message.ctx_api, message)
        except VKAPIError[18] as error:
            logger.error(f"[ID{message.ctx_api.xxx.user_id} {error}]")
            message.ctx_api.xxx.polling.stop()
        except VKAPIError[5] as error:
            logger.error(f"[ID{message.ctx_api.xxx.user_id} {error}]")
            message.ctx_api.xxx.polling.stop()
        except Exception as error:
            logger.error(f"[ID{message.ctx_api.xxx.user_id} {error}]")
            await asyncio.sleep(15)
    return wrapper


def vkontakte_on_error_scripts(func):
    @wraps(func)
    async def wrapper(session, user_id):
        try:
            return await func(session, user_id)
        except VKAPIError[18] as error:
            logger.error(f"[ID{session.xxx.user_id} {error}]")
            session.xxx.scripts.stop()
        except VKAPIError[5] as error:
            logger.error(f"[ID{session.xxx.user_id} {error}]")
            session.xxx.scripts.stop()
        except Exception as error:
            logger.error(f"[ID{session.xxx.user_id} {error}]")
            await asyncio.sleep(30)
    return wrapper
