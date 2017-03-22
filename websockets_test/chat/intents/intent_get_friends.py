import json

from channels import Group

from chat.Utils import get_friends
from chat.intents.base_intent import BaseIntent
from chat.models import Conversation


class IntentGetFriends(BaseIntent):
    def __init__(self):
        BaseIntent.__init__(self, "get_friends")

    def execute(self, message, message_data):
        Conversation.objects.filter(participants__in=message.user)
        Group("chat-%s" % message.user.username).send({

            "text": json.dumps({'intent': self.name, 'friends': get_friends(message.user)})
        })
