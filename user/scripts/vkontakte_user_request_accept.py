import asyncio
import random

from config import ProjectVar
from user.decorators import vkontakte_on_error_scripts


@vkontakte_on_error_scripts
async def request_accept(session, user_id):
    print("request_accept start")
    # Добавление друзей
    # await asyncio.sleep(30)
    while True:
        if not ProjectVar.USERS[user_id].script.get_condition("dr"):
            await asyncio.sleep(random.randint(600, 1800))
            continue
        followers = await session.api.request(method="friends.getRequests", data=dict(count=5))
        print(followers)
        if followers["response"]["count"] > 0:
            inject = await session.api.request(method="users.get", data=dict(user_ids=followers["response"]["items"]))
            for user in inject["response"]:
                if user.get("deactivated") is None:
                    await session.api.request(method="friends.add", data=dict(user_id=user["id"]))
                    await ProjectVar.USERS[user_id].script.set_stats("dr", 1)
                else:
                    await session.api.request(method="account.ban", data=dict(owner_id=user["id"]))
                await asyncio.sleep(3)
        await asyncio.sleep(60, 120)
