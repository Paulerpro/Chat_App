from rest_framework import routers

from apps.user.views import UserProfileViewset
from apps.friendship.views import FriendShipViewset

router = routers.DefaultRouter()

router.register(r"user", UserProfileViewset, basename="user")
router.register(r"friendship", FriendShipViewset, basename="friendship")