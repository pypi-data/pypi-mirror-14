from django.contrib.auth.models import User
from django.db import models


class Message(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, related_name="messages")
    socket = models.CharField(max_length=255, null=True, blank=True)
    title = models.CharField(max_length=255)
    # status = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    link = models.CharField(max_length=255, null=True, blank=True)
    link_text = models.CharField(max_length=255, null=True, blank=True)
    # percent = models.FloatField(null=True, blank=True)
    tag = models.CharField(max_length=255, null=True, blank=True)
