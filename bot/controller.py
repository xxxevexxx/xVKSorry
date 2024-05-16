import asyncio

from vkbottle import API
from loguru import logger
from utils import decrypt_data
from models.botmodel import Bots
from bot.command import bot_labeleres
from vkbottle.bot import Bot, BotLabeler
from vkbottle import BuiltinStateDispenser


class BotController:

    def __init__(self, bot_id: int):
        self.bot_id = bot_id
        self.polling = None
        self.client = None

    async def init(self):
        data = await Bots.filter(bot=self.bot_id).first()
        try:
            self.session(data)
            self.polling = BotPolling(self.client)
            self.polling.start()
        except Exception as error:
            logger.info(f"[BOT] Error init request: {error}")
            return False
        else:
            logger.info(f"[BOT] Success init request: {self.bot_id}")
            return True

    def session(self, data):
        bot = BotLabeler()
        for labeler in bot_labeleres:
            bot.load(labeler)
        self.client = Bot(
            api=API(token=decrypt_data(data.token)),
            labeler=bot,
            state_dispenser=BuiltinStateDispenser(),
        )

    def start(self):
        try:
            self.polling.start()
            logger.info(f"[BOT] Success start request: {self.bot_id}")
            return True
        except Exception as error:
            logger.error(f"[BOT] Error start request: {error}")
            return False

    def stop(self):
        try:
            self.polling.stop()
            logger.info(f"[BOT] Success stop request: {self.bot_id}")
            return True
        except Exception as error:
            logger.error(f"[BOT] Error stop request: {error}")
            return False

    def restart(self):
        try:
            self.polling.restart()
            logger.info(f"[BOT] Success restart request: {self.bot_id}")
            return True
        except Exception as error:
            logger.error(f"[BOT] Error restart request: {error}")
            return False


class BotPolling:

    def __init__(self, client):
        self.client = client
        self.task = None

    def start(self):
        if self.task is None:
            self.task = asyncio.create_task(self.client.run_polling())

    def stop(self):
        if self.task:
            self.task.cancel()
            self.task = None

    def restart(self):
        self.stop()
        self.start()
