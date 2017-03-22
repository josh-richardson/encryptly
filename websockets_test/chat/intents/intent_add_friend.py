from channels import Group
from django.contrib.auth.models import User

from chat.Utils import get_friends
from chat.intents.base_intent import BaseIntent
from chat.models import Contact
import json


class IntentAddFriend(BaseIntent):

    def __init__(self):
        BaseIntent.__init__(self, "add_friend")

    def execute(self, message, message_data):
        username = message_data['username']
        to_return = {'intent:': self.name, 'success': False, 'error': None}
        if username not in get_friends(message.user) and username != message.user.username:
            print(get_friends(message.user))
            user = User.objects.get(username=username)
            if user:
                contact = Contact()
                contact.from_user = message.user
                contact.to_user = user
                contact.save()
                to_return['success'] = True
            else:
                to_return['error'] = "Failure: no user with the specified username exists."
        else:
            to_return['error'] = "You are already friends with that user. You also can't add yourself as a friend."

        Group("chat-%s" % message.user.username).send({
            "text": json.dumps(to_return)
        })
