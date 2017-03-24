from functools import reduce

from channels import Group
from django.contrib.auth.models import User
from django.db.models import Count

from chat.Utils import get_friends
from chat.intents.base_intent import BaseIntent
from chat.models import Contact, Conversation, Message
import json


class IntentSendMessage(BaseIntent):
    def __init__(self):
        BaseIntent.__init__(self, "send_message")

    def execute(self, message, message_data):

        to_return = {'intent:': self.name, 'success': False, 'error': None}
        if 'conversation_id' in message_data:
            conversation_id = message_data['conversation_id']
            result = Conversation.objects.filter(id=conversation_id)
            if result.count() != 0:
                conv = result.first()
                if message.user in conv.participants:
                    new_message = Message()
                    new_message.content = message_data['content']
                    new_message.conversation = conv
                    new_message.save()
                    for p in conv.participants.all():
                        Group("chat-%s" % p.username).send({
                            "text": message.content['text']
                        })
                else:
                    to_return['error'] = "You do not have access to this conversation."

            elif 'username' in message_data:
                recipient_username = message_data['username']
                if recipient_username in get_friends(message.user) and recipient_username != message.user.username:
                    recipient = User.objects.get(username=recipient_username)
                    conv = Conversation()
                    conv.save()
                    conv.participants.add(recipient)
                    conv.participants.add(message.user)
                    new_message = Message()
                    new_message.content = message_data['content']
                    new_message.conversation = conv
                    new_message.save()
                    conv.save()
                    for p in conv.participants.all():
                        Group("chat-%s" % p.username).send({
                            "text": message.content['text']
                        })
                else:
                    to_return['error'] = "You cannot speak with this user as you are not friends with the user."
        else:
            to_return['error'] = "You appear to have sent a malformed request."

        Group("chat-%s" % message.user.username).send({
            "text": json.dumps(to_return)
        })
