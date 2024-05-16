import asyncio
import random

from config import ProjectVar
from user.decorators import vkontakte_on_error_scripts


@vkontakte_on_error_scripts
async def clear_subscriber(session, user_id):
    # Чистка подписок
    await asyncio.sleep(30)
    while True:
        if not ProjectVar.USERS[user_id].script.get_condition("ot"):
            await asyncio.sleep(random.randint(600, 1800))
            continue
        data = await session.api.request(method="friends.getRequests", data=dict(count=1000, out=1))
        if data["response"]["count"] > 150:
            list_user_id = data["response"]["items"][150:]
            if len(list_user_id) > 20:
                script = f"var user_ids = 1;"
                for enum, delete in enumerate(list_user_id):
                    script += "API.friends.delete({user_id: %s});" % delete
                    if enum == 20: break
                script += "return user_ids;"
                await session.api.execute(script)
                await ProjectVar.USERS[user_id].script.set_stats("ot", 20)
        await asyncio.sleep(60, 120)
