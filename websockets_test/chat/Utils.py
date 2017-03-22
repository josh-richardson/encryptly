from django.contrib.auth.models import User
from django.db.models import Q

from chat.models import Contact


def get_friends(user):
    return [contact.to_user.username for contact in user.contacts.all()]