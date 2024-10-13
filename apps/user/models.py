from django.db import models
from django.contrib.auth.models import User

from classes.base_model import BaseModel

class UserProfile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=220, blank=True, null=True)
    profile_picture = models.URLField(blank=True, null=True)
    email_verified = models.BooleanField(default=False)
