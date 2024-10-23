from channels.generic.websocket import WebsocketConsumer

from apps.chat.models import *

from asgiref.sync import async_to_sync

from django.shortcuts import get_object_or_404

import json

class ChatRoomConsumer(WebsocketConsumer):

    def connect(self):
        self.user = self.scope['user']
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.chatgroup = get_object_or_404(ChatGroup, group_name=self.room_name)

        # Create a channel layer group for the chat room
        async_to_sync(self.channel_layer.group_add)(
            self.room_name, self.channel_name
        )

        self.accept()

    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_name, self.channel_name
        )

    def receive(self, text_data=None):
        formatted_text_data = json.loads(text_data)
        body = formatted_text_data['body']

        message = GroupMessage.objects.create(
            body=body,
            author=self.user,
            group=self.chatgroup
        )

        event = {
            "type": 'chat_message',
            "message": message
        }

        # broadcast message to channels of the group
        async_to_sync(self.channel_layer.group_send)(
            self.room_name, event
        )

    def chat_message(self, event):
        
        context = {
            'user': self.user,
            'message': event["message"],
        }

        self.send(text_data=json.dumps(context))