from datetime import datetime

from django.db import models
from django.contrib.auth.models import User


class Contact(models.Model):
    owner_user = models.ForeignKey(User, related_name='contacts')
    contact = models.OneToOneField(User)


class Conversation(models.Model):
    id = models.AutoField(primary_key=True)
    date_started = models.DateTimeField(blank=True, default=datetime.now())
    participants = models.ManyToManyField(User, related_name='conversations')


class Message(models.Model):
    content = models.CharField(max_length=4096)
    conversation = models.ForeignKey(Conversation, related_name='messages')