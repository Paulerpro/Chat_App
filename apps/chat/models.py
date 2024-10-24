from django.db import models
from django.contrib.auth.models import User

from classes.base_model import BaseModel

from apps.chat.managers import ChatGroupManager

import shortuuid

class ChatGroup(BaseModel):
    group_name = models.CharField(max_length=200, unique=True, default=shortuuid.uuid())
    admin = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    members = models.ManyToManyField(User, related_name="members_in_group", blank=True)

    objects = ChatGroupManager()

    def __str__(self):
        return self.group_name

class GroupMessage(BaseModel):
    group = models.ForeignKey(ChatGroup, on_delete=models.CASCADE, related_name='group_messages')
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    body = models.TextField(blank=True, null=True)
    file = models.FileField(upload_to="files/", blank=True, null=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        if self.body:
            return f"{self.author.username} : {self.body[:28]}"
        if self.file:
            return f"{self.author.username} : {self.file}"
