from django.urls import path
# from django.contrib.auth.views import LoginView, LogoutView

from apps.user.views import RegisterView, LoginView, LogoutView

urlpatterns = [
    path('register-user/', RegisterView.as_view(), name="register-user"),
    path('login-user/', LoginView.as_view(), name="login-user"),
    path('logout-user/', LogoutView.as_view(), name="logout-user"),
]