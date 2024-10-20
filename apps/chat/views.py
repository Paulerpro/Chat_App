from django.shortcuts import get_object_or_404

from rest_framework import viewsets, generics
from rest_framework.response import Response
from rest_framework.decorators import action

from apps.chat.models import ChatGroup, GroupMessage
from apps.chat.serializers import GroupMessageSerializer

from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiParameter

class ChatViewset(viewsets.ViewSet, generics.GenericAPIView):

    def get_serializer_class(self):
        if self.action in [
            'get_group_messages',
            'send_group_message'
        ]:
            return GroupMessageSerializer
        
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
