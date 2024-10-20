from django.shortcuts import render
from django.contrib.auth.models import AnonymousUser

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.friendship.models import Friendship
from apps.friendship.serializers import FriendshipSerializer
from apps.user.models import UserProfile

# add friend (post) check for duplicates
#  get all requests for from_user
# get all requests for to_user
# accept/decline f-request (put/patch)
# block existing friend
# notfy users when friend request sent

class FriendShipViewset(viewsets.ViewSet):
    queryset = Friendship.objects.all()
    serializer_class = FriendshipSerializer
    # permission_classes = 

    @action(detail=False, methods=["post"], url_path="add-friend")
    def add_friend(self, request):
        user = request.user
        # to_user_id = request.data.get("to_user")
        # to_user = UserProfile.objects.filter(to_user_id).first()

        serializer = FriendshipSerializer(data=request.data, many=False)
        if serializer.is_valid():
            instance = serializer.save(from_user=user)
            instance.save()
            return Response({"message": "Friend request sent"}, 200)
        return Response(serializer.errors, 400)

    @action(detail=False, methods=["get"], url_path="get-user-received-requests")
    def get_user_received_requests(self, request):
        if request.user == AnonymousUser:
            return Response({"Kindly log in to view"}, 400)
        friend_requests = self.queryset.filter(to_user=request.user.id)
        serializer = FriendshipSerializer(friend_requests, many=True)
        
        return Response(serializer.data, 200)
        
    @action(detail=False, methods=["put"], url_path="handle-friend-request")
    def handle_friend_request(self, request):
        request_id = request.data.get("request_id", None)
        action = request.data.get("action", None)

        try:
            request = self.queryset.filter(id=request_id).first()
            request.status = action

            # if action == "BLOCKED":
            # terminate ongoing chats between users
            #     pass

            request.save()
            return Response({f"Instance successfully set to {action}"}, 200)
        except Exception as e:
            return Response({"message": f"{e}"}, 400)

    # @action()
    # def block_friend(self, request):
    #     pass

