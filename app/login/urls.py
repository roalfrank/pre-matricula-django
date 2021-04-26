from django.urls import path
from django.contrib.auth.views import LogoutView, LoginView
from .views import LoginFormView

app_name = "login"

urlpatterns = [
    path("", LoginFormView.as_view(), name="login-user"),
    path("logout/", LogoutView.as_view(), name="logout")

]
