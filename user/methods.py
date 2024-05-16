from vkbottle.user import Message


class Methods:

    def __init__(self, client):
        self.client = client

    async def send(self, message: Message, for_id: int, text: str):
        await self.client.messages.send(
            peer_id=for_id,
            message=text,
            random_id=0
        )

    async def edit(self, message: Message, text: str):
        return await self.client.messages.edit(
            peer_id=message.peer_id,
            message_id=message.id,
            message=text
        )

    async def delete(self, message: Message):
        await self.client.messages.delete(
            peer_id=message.from_id,
            message_ids=message.id,
            delete_for_all="1" if message.from_id != message.peer_id else "0"
        )
