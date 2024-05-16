import asyncio
import random

from config import ProjectVar
from user.decorators import vkontakte_on_error_scripts


@vkontakte_on_error_scripts
async def like_subscriber(session, user_id):
    # Лайк уведомлений
    await asyncio.sleep(30)
    while True:
        if not ProjectVar.USERS[user_id].script.get_condition("li"):
            await asyncio.sleep(random.randint(600, 1800))
            continue
        data = await session.api.request(method="newsfeed.getSubscribersFeed", data=dict(count=1))
        if data["response"]["items"]:
            if data["response"]["items"][0]["likes"]["user_likes"] == 0:
                await session.api.request(
                    method="likes.add",
                    data=dict(
                        type="post",
                        owner_id=data["response"]["items"][0]["source_id"],
                        item_id=data["response"]["items"][0]["post_id"]
                    )
                )
                await ProjectVar.USERS[user_id].script.set_stats("li", 1)
        await asyncio.sleep(120, 300)
