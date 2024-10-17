from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate

from rest_framework import generics, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response

from apps.user.models import UserProfile
from apps.user.serializers import UserProfileSerializer

class RegisterView(generics.CreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

class LoginView(APIView):

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return Response({'message': 'User logged in'}, 200)
        return Response({"User doesn't exist"}, 400)
class LogoutView(APIView):

    def post(self, request):
        logout(request)
        return Response({"Looged out successfully"}, 200)

class UserProfileViewset(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

    # Decide if soft delete or hard