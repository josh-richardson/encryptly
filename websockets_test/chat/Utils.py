from django.contrib.auth.models import User
from django.db.models import Q

from chat.models import Contact


def get_friends(user):
    return [contact.contact.username for contact in user.contacts.all()]