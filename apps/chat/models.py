from django.db import models
from django.contrib.auth.models import User

from classes.base_model import BaseModel

class ChatGroup(BaseModel):
    group_name = models.CharField(max_length=200, unique=True)
    members = models.ManyToManyField(User, related_name="members_in_group", blank=True)

    def __str__(self):
        return self.group_name

class GroupMessage(BaseModel):
    group = models.ForeignKey(ChatGroup, on_delete=models.CASCADE, related_name='group_messages')
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    body = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.author.username} : {self.body[:28]}"
