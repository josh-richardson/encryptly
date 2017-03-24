import json

from channels import Group

from chat.Utils import get_friends
from chat.intents.base_intent import BaseIntent
from chat.models import Conversation


class IntentGetConversations(BaseIntent):
    def __init__(self):
        BaseIntent.__init__(self, "get_conversations")

    def execute(self, message, message_data):
        conversations = []
        conversation_contacts = []
        for conversation in Conversation.objects.filter(participants__in=[message.user]).all():
            i_conversation_contacts = [participant.username for participant in conversation.participants.iterator()]
            conversations.append({"id": conversation.id, "users": i_conversation_contacts})
            conversation_contacts.extend(i_conversation_contacts)

        remaining_friends = get_friends(message.user)
        for existing_friend in conversation_contacts:
            if existing_friend in remaining_friends:
                remaining_friends.remove(existing_friend)

        Group("chat-%s" % message.user.username).send({
            "text": json.dumps({'intent': self.name, "conversations": conversations, "remaining_friends": remaining_friends})
        })
