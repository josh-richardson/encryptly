import json

from channels import Group

from chat.Utils import get_friends
from chat.intents.base_intent import BaseIntent
from chat.models import Conversation


class IntentGetMessages(BaseIntent):
    def __init__(self):
        BaseIntent.__init__(self, "get_messages")

    def execute(self, message, message_data):
        print("fired")
        to_return = {"intent": self.name, "messages": None, "error": None}
        messages = []
        conversation_id = message_data['conversation']
        conversation = Conversation.objects.get(id=conversation_id)
        if message.user.conversations.contains(conversation):
            for m in conversation.messages:
                messages.append(m)
            to_return['messages'] = messages
        else:
            to_return['error'] = "You do not have access to this conversation."

        Group("chat-%s" % message.user.username).send({
            "text": json.dumps(to_return)
        })
