from django.urls import path
from .views import get_user, sign_up, login, logout, update_access_token

urlpatterns = [
    path("register", sign_up, name="register"),
    path("login/", login, name="login"),
    path("logout", logout, name="logout"),
    path("refresh", update_access_token, name="refresh"),
    path("me", get_user, name="get_users"),
]
