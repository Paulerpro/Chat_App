from django.db import models
from django.db.models.query import QuerySet

class ChatGroupManager(models.Manager):

    def get_group_chat(self, group_name) -> QuerySet:
        return super().get_queryset().filter(group_name=group_name).first()