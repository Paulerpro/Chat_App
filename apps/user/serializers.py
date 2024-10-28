from rest_framework import serializers

from apps.user.models import UserProfile

from django.contrib.auth.models import User

from .tasks import send_confirmation_email

class UserSerializer(serializers.ModelSerializer):
   class Meta:
      model = User
      fields = [
         "id",
         "username",
         "email",
         "password",
         "first_name",
         "last_name"
      ]

   def create(self, validated_data):
         user = super().create(validated_data)

         UserProfile.objects.create(user=user)

         send_confirmation_email.delay()

         return user
class UserProfileSerializer(serializers.ModelSerializer):
     class Meta:
        model = UserProfile
        fields = "__all__"