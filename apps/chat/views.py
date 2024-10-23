from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.db.models import Count

from rest_framework import viewsets, generics
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny

from apps.chat.models import ChatGroup, GroupMessage
from apps.chat.serializers import GroupMessageSerializer, ChatGroupSerializer

from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiParameter

class ChatViewset(viewsets.ViewSet, generics.GenericAPIView):
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        if self.action in [
            'get_group_messages',
            'send_group_message'
        ]:
            return GroupMessageSerializer
        if self.action in [
            "get_or_create_private_chat",
        ]:
            return ChatGroupSerializer
        
    def get_queryset(self):
        if self.action in [
            'get_group_messages',
            'send_group_message'
        ]:
            return GroupMessage.objects.all()

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="group_name",
                description="filter group messages by group name",
                type=str,
                required=True,
                # enum=
            )
        ]
    )
    @action(detail=False, methods=["get"], url_path="get-group-messages")
    def get_group_messages(self, request):
        group_name = request.GET.get("group_name", None)
        try:
            group = get_object_or_404(ChatGroup, group_name=group_name)
            queryset = group.group_messages.all()
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data, 200)
        except Exception as e:
            return Response(f"{e}", 200)
    
    @extend_schema(
        request="",
        examples=[
            OpenApiExample(
                name="Example payload",
                description="sample payload",
                value={
                    "group": "2",
                    "body": "lorem ipsum"
                }
            )
        ]
    )
    @action(detail=False, methods=["post"], url_path="send-group-message")
    def send_group_message(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response({"Message sent"}, 200)
        return Response(serializer.errors, 400)
    
    # create group
    # add group memebers

    # private chat (2 members only)
    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="username",
                description="get private by other_member_username",
                type=str,
                required=True,
                # enum=
            )
        ]
    )
    @action(detail=False, methods=["get"], url_path="private-chat")
    def get_or_create_private_chat(self, request):
        username = request.GET.get("username", None)

        try:
            other_member = User.objects.get(username=username)
        except Exception as e:
            return Response(f'{e}', 404)

        # Query group containing exactly these two members
        private_room = ChatGroup.objects.filter(
            members__in=[other_member, request.user]
        ).annotate(
            num_members=Count('members')
        ).filter(num_members=2).first()

        if not private_room:
            print("To be created")
            private_room = ChatGroup.objects.create(
                group_name=f"{request.user.username} & {other_member.username} chat"
                )
            private_room.members.add(other_member, request.user)

        serializer = self.get_serializer(private_room, many=False)

        return Response(serializer.data, 200)