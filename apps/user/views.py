from django.shortcuts import render
from rest_framework import generics

class RegisterView(generics.CreateAPIView):
    queryset = ""
    serializer_class = ""

class LoginView():
    pass