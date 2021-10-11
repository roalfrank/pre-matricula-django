import json
from asyncio import sleep
from channels.generic.websocket import AsyncWebsocketConsumer


class ComentariosMatricula(AsyncWebsocketConsumer):
    async def connect(self):
        self.matricula = self.scope['url_route']['kwargs']['matricula']
        self.group_name = f'comentario_matricula_{self.matricula}'
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def send_message(self, event):
        await self.send(text_data=json.dumps({'comentario': event}))


class MatriculaUpdate(AsyncWebsocketConsumer):
    async def connect(self):
        self.matricula = self.scope["url_route"]["kwargs"]["matricula"]
        self.group_name = f'update_matricula_{self.matricula}'

        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def send_message(self, event):
        await self.send(text_data=json.dumps({'matricula': event}))


class LikeMatricula(AsyncWebsocketConsumer):
    async def connect(self):
        self.matricula = self.scope["url_route"]["kwargs"]["matricula"]
        self.group_name = f'like_matricula_{self.matricula}'

        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def send_message(self, event):
        contador_like = event['contador_like']
        await self.send(text_data=json.dumps({'contador_like': contador_like}))
