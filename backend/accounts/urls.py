from django.urls import path

from .views import (
    RegisterView,
    LoginView,
    MeView,
    SendOTPView,
    VerifyOTPView,
    SessionListView,
    SessionLogoutView,
    LogoutAllSessionsView,
)


urlpatterns = [

    path(
        "register/",
        RegisterView.as_view()
    ),

    path(
        "login/",
        LoginView.as_view()
    ),

    path(
        "send-otp/",
        SendOTPView.as_view()
    ),

    path(
        "verify-otp/",
        VerifyOTPView.as_view()
    ),

    path(
        "me/",
        MeView.as_view()
    ),

    path(
        "sessions/",
        SessionListView.as_view()
    ),

    path(
        "sessions/logout/",
        SessionLogoutView.as_view()
    ),

    path(
        "logout-all/",
        LogoutAllSessionsView.as_view()
    ),

]