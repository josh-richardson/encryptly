import json

import time
from channels import Group

from chat.intents.base_intent import BaseIntent
from chat.models import Conversation


class IntentGetMessages(BaseIntent):
    def __init__(self):
        BaseIntent.__init__(self, "get_messages")

    def execute(self, message, message_data):
        to_return = {"intent": self.name, "messages": None, "conversation": None, "error": None}
        messages = []
        conversation_id = message_data['conversation']
        conversation = Conversation.objects.get(id=conversation_id)
        if message.user.conversations.filter(id=conversation.id).exists():
            to_return['conversation'] = message_data['conversation']
            for m in conversation.messages.all():
                msg_dict = {"date_sent": time.mktime(m.date_sent.timetuple()), "content": m.content, "username": m.from_user.username}
                messages.append(msg_dict)
            to_return['messages'] = messages
        else:
            to_return['error'] = "You do not have access to this conversation."

        Group("chat-%s" % message.user.username).send({
            "text": json.dumps(to_return)
        })
