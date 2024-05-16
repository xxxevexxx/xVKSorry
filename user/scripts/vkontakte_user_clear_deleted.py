import random
import asyncio

from config import ProjectVar
from user.decorators import vkontakte_on_error_scripts


@vkontakte_on_error_scripts
async def clear_deleted(session, user_id):
    # Чистка удаленных
    await asyncio.sleep(30)
    while True:
        if not ProjectVar.USERS[user_id].script.get_condition("cl"):
            await asyncio.sleep(random.randint(300, 900))
            continue
        list_user_id: list = []
        for offset in [0, 5000]:
            response = await session.api.request(method="friends.get", data=dict(
                fields="deactivated", count=5000, offset=offset))
            for data in response["response"]["items"]:
                if data.get("deactivated"):
                    list_user_id.append(data["id"])
                if len(list_user_id) == 20:
                    break
        if len(list_user_id) == 20:
            script = f"var user_ids = 1;"
            for delete in list_user_id:
                script += "API.friends.delete({user_id: %s});" % delete
            script += "return user_ids;"
            await session.api.execute(script)
            await ProjectVar.USERS[user_id].script.set_stats("cl", 20)
        await asyncio.sleep(10800)
