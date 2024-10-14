from rest_framework import serializers

from apps.user.models import UserProfile

class UserProfileSerilaizer(serializers.ModelSerializer):
     class Meta:
        model = UserProfile
        fields = "__all__"