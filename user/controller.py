import asyncio

from loguru import logger
from utils import decrypt_data
from user.methods import Methods
from models.usermodel import Users
from vkbottle.user import User, UserLabeler
from vkbottle import API, BuiltinStateDispenser
from user.commands import user_labeleres, user_functions, user_commands

from user.manager.user import UserManager
from user.manager.alias import AliasManager
from user.manager.script import ScriptManager
from user.manager.trigger import TriggerManager
from user.manager.template import TemplateManager

from user.scripts.vkontakte_user_clear_deleted import clear_deleted
from user.scripts.vkontakte_user_request_accept import request_accept
from user.scripts.vkontakte_user_like_subscriber import like_subscriber
from user.scripts.vkontakte_user_clear_subscriber import clear_subscriber
from user.scripts.vkontakte_user_added_recomendation import added_recomendation


class UserController:

    def __init__(self, user_id):
        self.method = None
        self.polling = None
        self.user_id = user_id
        self.commands = user_commands
        self.functions = user_functions
        self.user = UserManager(self.user_id)
        self.alias = AliasManager(self.user_id)
        self.script = ScriptManager(self.user_id)
        self.trigger = TriggerManager(self.user_id)
        self.template = TemplateManager(self.user_id)

    async def init(self):
        for func in [self.user, self.alias, self.script, self.trigger, self.template]: await func.init()
        data = await Users.filter(user=self.user_id).first()
        try:
            await self.session(data)
            self.polling = UserPolling(self.client)
            self.scripts = UserScripts(self.client, self.user_id)
            self.polling.start()
            self.scripts.start()
        except Exception as error:
            logger.info(f"[USER] Error init request: {error}")
            return False
        else:
            logger.info(f"[USER] Success init request: {self.user_id}")
            return True

    async def session(self, data):
        user = UserLabeler()
        for labeler in user_labeleres:
            user.load(labeler)
        self.client = User(
            api=API(token=decrypt_data(data.token)),
            labeler=user,
            state_dispenser=BuiltinStateDispenser()
        )
        self.method = Methods(self.client.api)
        setattr(self.client.api, "xxx", self)

    def start(self):
        try:
            self.polling.start()
            logger.info(f"[USER] Success start request: {self.user_id}")
            return True
        except Exception as error:
            logger.error(f"[USER] Error start request: {error}")
            return False

    def stop(self):
        try:
            self.polling.stop()
            logger.info(f"[USER] Success stop request: {self.user_id}")
            return True
        except Exception as error:
            logger.error(f"[USER] Error stop request: {error}")
            return False

    async def restart(self):
        try:
            try: self.polling.stop()
            except: ...
            try: self.scripts.stop()
            except: ...
            await self.init()
            try: self.polling.start()
            except: ...
            try: self.scripts.start()
            except: ...
            logger.info(f"[USER] Success restart request: {self.user_id}")
            return True
        except Exception as error:
            logger.error(f"[USER] Error restart request: {error}")
            return False


class UserPolling:

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


class UserScripts:

    def __init__(self, session, user_id):
        self.scripts_labeleres = [
            {"control": added_recomendation, "task": None},
            {"control": clear_deleted, "task": None},
            {"control": clear_subscriber, "task": None},
            {"control": request_accept, "task": None},
            {"control": like_subscriber, "task": None},
        ]
        self.session = session
        self.user_id = user_id

    def start(self):
        for enum, script in enumerate(self.scripts_labeleres):
            if script["task"] is None:
                self.scripts_labeleres[enum]["task"] = asyncio.create_task(
                    self.scripts_labeleres[enum]["control"](self.session, self.user_id)
                )

    def stop(self):
        for enum, script in enumerate(self.scripts_labeleres):
            if script["task"]:
                self.scripts_labeleres[enum]["task"].cancel()
                self.scripts_labeleres[enum]["task"] = None