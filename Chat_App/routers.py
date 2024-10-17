from rest_framework import routers

from apps.user.views import UserProfileViewset

router = routers.DefaultRouter()

router.register(r"user", UserProfileViewset, basename="user")