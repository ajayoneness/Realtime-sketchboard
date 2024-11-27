import json
from channels.generic.websocket import AsyncWebsocketConsumer

class BoardConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = "board"
        self.room_group_name = f"board_{self.room_name}"

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive drawing data from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        action = text_data_json["action"]
        coordinates = text_data_json["coordinates"]

        # Send the drawing data to the group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'send_drawing',
                'action': action,
                'coordinates': coordinates,
            }
        )

    # Receive message from room group
    async def send_drawing(self, event):
        action = event['action']
        coordinates = event['coordinates']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'action': action,
            'coordinates': coordinates,
        }))
