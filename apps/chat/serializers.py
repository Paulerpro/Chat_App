from rest_framework import serializers

from apps.chat.models import GroupMessage, ChatGroup

class GroupMessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = GroupMessage
        fields = "__all__"

class ChatGroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = ChatGroup
        fields = "__all__"