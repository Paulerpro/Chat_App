from django.contrib import admin

from apps.chat.models import ChatGroup, GroupMessage

admin.site.register(ChatGroup)
admin.site.register(GroupMessage)