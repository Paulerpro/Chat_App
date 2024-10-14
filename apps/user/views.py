from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response

from apps.user.serializers import UserProfileSerilaizer

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserProfileSerilaizer

class LoginView(APIView):

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return Response({'message': 'User logged in'}, 200)
        return Response({"User doesn't exist"}, 400)

