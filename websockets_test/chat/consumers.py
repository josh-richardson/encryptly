import json

from channels import Group
from channels.auth import channel_session_user_from_http, channel_session_user

from chat.intents.intent_add_friend import IntentAddFriend

# receive message from user with chat id -> map chat ID to list of active user sessions -> emit to those sessions only
from chat.intents.intent_get_conversations import IntentGetConversations
from chat.intents.intent_send_message import IntentSendMessage

intents = [IntentAddFriend(), IntentGetConversations(), IntentSendMessage()]
@channel_session_user
def ws_message(message):
    if message.user.is_authenticated():
        message_data = json.loads(message.content['text'])
        for intent in intents:
            if intent.validate(message_data["intent"]):
                intent.execute(message, message_data)

        # Group("chat-%s" % message.channel_session['room']).send({
        #     "text": message.content['text']
        # })


@channel_session_user_from_http
def ws_connect(message):
    if message.user.is_authenticated():
        message.reply_channel.send({"accept": True})
        Group("chat-%s" % message.user.username).add(message.reply_channel)


@channel_session_user
def ws_disconnect(message):
    if message.user.is_authenticated():
        Group("chat-%s" % message.user.username).discard(message.reply_channel)
