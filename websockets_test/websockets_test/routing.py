from channels.routing import route

from chat.consumers import ws_message, ws_disconnect, ws_add

channel_routing = [
    route('websocket.receive', ws_message),
    route('websocket.connect', ws_add),
    route('websocket.disconnect', ws_disconnect)
]