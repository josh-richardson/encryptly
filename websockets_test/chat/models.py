from datetime import datetime

from django.db import models
from django.contrib.auth.models import User


class Contact(models.Model):
    id = models.AutoField(primary_key=True)
    from_user = models.ForeignKey(User, related_name='contacts')
    to_user = models.ForeignKey(User, related_name='unused_contact')

    class Meta:
        unique_together = ('to_user', 'from_user')


class Conversation(models.Model):
    id = models.AutoField(primary_key=True)
    date_started = models.DateTimeField(blank=True, default=datetime.now())
    participants = models.ManyToManyField(User, related_name='conversations')


class Message(models.Model):
    from_user = models.ForeignKey(User, related_name='sent_messages')
    date_sent = models.DateTimeField(blank=True, default=datetime.now())
    content = models.CharField(max_length=4096)
    conversation = models.ForeignKey(Conversation, related_name='messages')