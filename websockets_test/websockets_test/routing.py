from channels.routing import route

from chat.consumers import ws_message, ws_disconnect, ws_connect

channel_routing = [
    route('websocket.receive', ws_message),
    route('websocket.connect', ws_connect),
    route('websocket.disconnect', ws_disconnect)
]