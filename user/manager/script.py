from models.usermodel import Users, Scripts
from loguru import logger


class ScriptManager:

    def __init__(self, user_id):
        self.user_id = user_id
        self.user = None
        self.scripts = None
        self.data_scripts = {
            "stats": {
                "li": None, "dr": None, "uv": None, "ot": None, "cl": None, "ar": None
            },
            "condition": {
                "li": None, "dr": None, "uv": None, "ot": None, "cl": None, "ar": None
            }
        }

    async def init(self):
        self.user = await Users.filter(user=self.user_id).first()
        data = await Scripts.filter(user=self.user).first()
        self.data_scripts["stats"]["li"] = data.stats_li
        self.data_scripts["stats"]["dr"] = data.stats_dr
        self.data_scripts["stats"]["uv"] = data.stats_uv
        self.data_scripts["stats"]["ot"] = data.stats_ot
        self.data_scripts["stats"]["cl"] = data.stats_cl
        self.data_scripts["stats"]["ar"] = data.stats_ar
        self.data_scripts["condition"]["li"] = data.condition_li
        self.data_scripts["condition"]["dr"] = data.condition_dr
        self.data_scripts["condition"]["uv"] = data.condition_uv
        self.data_scripts["condition"]["ot"] = data.condition_ot
        self.data_scripts["condition"]["cl"] = data.condition_cl
        self.data_scripts["condition"]["ar"] = data.condition_ar

    def get_stats(self, name):
        return self.data_scripts["stats"][name]

    def get_condition(self, name):
        return self.data_scripts["condition"][name]

    async def set_stats(self, name, value):
        self.data_scripts["stats"][name] += value
        await Scripts.filter(user=self.user).update(**{f"stats_{name}": self.data_scripts["stats"][name]})

    async def set_condition(self, name, value):
        self.data_scripts["condition"][name] = value
        logger.info(self.data_scripts["condition"][name])
        await Scripts.filter(user=self.user).update(**{f"condition_{name}": value})
