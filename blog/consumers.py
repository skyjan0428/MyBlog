from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer
import json
from .models import Client, User, Token, Message
class Consumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = 'testroom'
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        try:
            token = Token.objects.get(token=self.scope['cookies']['token'])
            self.room_name = token.user_id.user_id
            client = Client(channel_name = self.channel_name, user_id = token.user_id)
            client.save()
        except Exception as e:
            print(str(e))

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        client = Client.objects.get(channel_name=self.channel_name)
        client.delete()

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        user_id = text_data_json['user_id']
        message = text_data_json['message']
        user = User.objects.get(user_id=self.room_name)
        receivers = Client.objects.filter(user_id = user_id)
        for receiver in receivers:
            await self.channel_layer.send(receiver.channel_name, {
                "type": "chat_message",
                "message": message,
                "sender": user.name
            })
        message = Message(sender=user, reciever=receivers.first().user_id, text=message)
        message.save()
        

        # Send message to room group
        # await self.channel_layer.group_send(
        #     self.room_group_name,
        #     {
        #         'type': 'chat_message',
        #         'message': message
        #     }
        # )

    async def chat_message(self, event):
        message = event['message']
        print(message)
        # Send message to WebSocket
        # await self.channel_layer.send(self.channel_name, {
        #     "message": "message",
        # })
        await self.send(text_data=json.dumps({
            'message': message,
            'sender':event['sender']
        }))






# from channels.generic.websocket import WebsocketConsumer
# import json

# class Consumer(WebsocketConsumer):
#     def connect(self):
#         self.accept()

#     def disconnect(self, close_code):
#         pass

#     def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         message = '運維咖啡吧：' + text_data_json['message']

#         self.send(text_data=json.dumps({
#             'message': message
#         }))