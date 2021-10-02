import json
from asyncio import sleep
from channels.generic.websocket import AsyncWebsocketConsumer


class MatriculaUpdate(AsyncWebsocketConsumer):
    async def connect(self):
        self.matricula = self.scope["url_route"]["kwargs"]["matricula"]
        self.group_name = f'update_matricula_{self.matricula}'

        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def send_message(self, event):
        print('de adentro de mensaje el evento', event)
        await self.send(text_data=json.dumps({'matricula': event}))


class LikeMatricula(AsyncWebsocketConsumer):
    async def connect(self):
        self.matricula = self.scope["url_route"]["kwargs"]["matricula"]
        self.group_name = f'like_matricula_{self.matricula}'

        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    # async def receive(self, text_data):
    #     print('datos desde receive', text_data)
    #     json_data = json.loads(text_data)
    #     contador_like = json_data['contador_like']
    #     event = {
    #         'type': 'send_message',
    #         'contador_like': contador_like
    #     }
    #     await self.channel_layer.group_send(self.group_name, event)

    async def send_message(self, event):
        print(event)
        contador_like = event['contador_like']
        await self.send(text_data=json.dumps({'contador_like': contador_like}))
