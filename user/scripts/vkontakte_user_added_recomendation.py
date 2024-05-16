import random
import asyncio

from config import ProjectVar
from user.decorators import vkontakte_on_error_scripts


@vkontakte_on_error_scripts
async def added_recomendation(session, user_id):
    # Добавление рекомендаций
    await asyncio.sleep(30)
    while True:
        if not ProjectVar.USERS[user_id].script.get_condition("ar"):
            await asyncio.sleep(random.randint(600, 1800))
            continue
        fields: str = "common_count, is_friend, blacklisted_by_me, online"
        data: dict = await session.api.request(
            method="friends.getRecommendations", data=dict(filter="mutual", fields=fields)
        )
        user_list: list = []
        for user_data in data["response"]["items"]:
            if user_data["is_friend"] == 0 and user_data["blacklisted_by_me"] == 0 and user_data["online"] == 1:
                user_list.append([user_data["common_count"], user_data["id"]])
        user_list.sort()
        user_add = random.randint(3, 6)
        if len(user_list) > user_add:
            for _, user in user_list[-user_add:]:
                data: dict = await session.api.request(method="friends.add", data=dict(user_id=user))
                if data["response"] == 1:
                    await ProjectVar.USERS[user_id].script.set_stats("ar", 1)
                    await asyncio.sleep(3)
        await asyncio.sleep(400, 800)
