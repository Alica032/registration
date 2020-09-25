from django.urls import path
from django.contrib import admin

from . import views

urlpatterns = (
    [
        path("register/", views.RegisterView.as_view(), name="register"),
        path("activate/<token>/", views.LinkRegistrationView.as_view(), name="activate"),
        path("login/", views.user_login, name="login"),
        path("verify/", views.phone_verification_view, name="phone_verification"),
    ], "accounts", "accounts",
)
