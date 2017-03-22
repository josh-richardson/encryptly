from django.db import models
from django.contrib.auth.models import User


class Contact(models.Model):
    owner_user = models.ForeignKey(User, related_name='contacts')
    contact = models.OneToOneField(User)


class Conversation(models.Model):
    contacts = models.OneToOneField(Contact)


class Message(models.Model):
    content = models.CharField(max_length=4096)
    conversation = models.ForeignKey(Conversation, related_name='messsages')