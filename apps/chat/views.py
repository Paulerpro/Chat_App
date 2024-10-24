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

from channels.layers import get_channel_layer

from asgiref.sync import async_to_sync

class ChatViewset(viewsets.ViewSet, generics.GenericAPIView):
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        if self.action in [
            'get_chat_messages',
            'send_group_message'
        ]:
            return GroupMessageSerializer
        if self.action in [
            "get_or_create_private_chat",
            "create_group_chat",
            "edit-groupchat",
            "leave_chat_group"
        ]:
            return ChatGroupSerializer
        
    def get_queryset(self):
        if self.action in [
            'get_chat_messages',
            'send_group_message'
        ]:
            return GroupMessage.objects.all()
        if self.action in [
            'create_group_chat'
            "edit-groupchat",
            "leave_chat_group"
        ]:
            return ChatGroup.objects.all()

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
    @action(detail=False, methods=["get"], url_path="get-chat-messages")
    def get_chat_messages(self, request):
        group_name = request.data.get("group_name", None)

        group = self.get_queryset.get_group_chat(group_name)
        
        if group:
            queryset = group.group_messages.all()

            # add user if not member. New member joins via link
            if request.user not in group.members.all():
                group.members.add(request.user)
                group.save()

            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data, 200)
        return Response({"Gropu doesn't exist"}, 400)
    
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
    
    @action(detail=False, methods=["post"], url_path="send-file")
    def send_file(self, request):
        file = request.FILES.get("file", None)

        group_name = request.data.get("group_name", None)

        group = ChatGroup.objects.get_group_chat(group_name)

        if group:
            message = GroupMessage.objects.create(
                author=request.user,
                file=file,
                group=group
            )

            serialized_message = {
                "id": message.id,
                "file": message.file,
                "author": message.author.username,
            }

            channel_layer = get_channel_layer()

            event = {
                "type": "chat_message", # already defined in consumers.py
                "message": serialized_message
            }

            async_to_sync(channel_layer.group_send)(
                group_name, event
            )

            return Response({"file sent"}, 200)
        return Response({"Group doesn't exist"}, 400)

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

        # Query group containing exactly the two private members
        private_room = ChatGroup.objects.filter(
            members__in=[other_member, request.user]
        ).annotate(
            num_members=Count('members')
        ).filter(num_members=2).first()

        if not private_room:
            private_room = ChatGroup.objects.create(
                group_name=f"{request.user.username} & {other_member.username} chat"
                )
            private_room.members.add(other_member, request.user)

        serializer = self.get_serializer(private_room, many=False)

        return Response(serializer.data, 200)
    
    # create group
    @action(detail=False, methods=['post'], url_path="create-group-chat")
    def create_group_chat(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(admin=request.user, memebers=[request.user])     
            return Response({"Group created successfully"}, 200)   
        return Response(serializer.errors, 400)
    
    # delete chat_group
    @action(detail=False, methods=["delete"], url_path="delete-chat-group")
    def delete_group_chat(self, request):
        group_name = request.GET.get("group_name", None)
        try:
            group = get_object_or_404(ChatGroup, group_name=group_name)

            if request.user != group.admin:
                return Response({"Only admin can delete group"}, 400)
            
            group.delete()

            return Response({"Group deleted successfully"}, 200)
        except Exception as e:
            return Response(f"{e}", 200)
        
    # edit chatgroup
    @action(detail=False, methods=["put"], url_path="edit-groupchat")
    def edit_groupchat(self, request):
        group_name = request.data.get("group_name", None)

        group = self.get_queryset.get_group_chat(group_name)

        if group:
            serializer = self.get_serializer(instance=group, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, 200)
        return Response(serializer.errors, 400)
    
    # leave chatgroup
    @action(detail=False, methods=["put"], url_path="leave-chat-group")
    def leave_chat_group(self, request):
        group_name = request.data.get("group_name", None)

        group = self.get_queryset.get_group_chat(group_name)

        if group:
            group.members.remove(request.user)
            group.save()
            return Response({"user left group"}, 200)

        return Response({"Group doesn't exist"}, 400)
    
    