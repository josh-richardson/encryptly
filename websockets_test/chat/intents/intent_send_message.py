from channels import Group
from django.contrib.auth.models import User

from chat.Utils import get_friends
from chat.intents.base_intent import BaseIntent
from chat.models import Contact, Conversation
import json


class IntendSendMessage(BaseIntent):

    def __init__(self):
        BaseIntent.__init__(self, "send_message")

    def execute(self, message, message_data):
        username = message_data['username']
        to_return = {'intent:': self.name, 'success': False, 'error': None}
        if username in get_friends(message.user) and username is not message.user.username:
            pass
            # if Conversation.objects.filter(contact)
        else:
            to_return['error'] = "You are already friends with that user. You also can't add yourself as a friend."

        Group("chat-%s" % message.user.username).send({
            "text": json.dumps(to_return)
        })
