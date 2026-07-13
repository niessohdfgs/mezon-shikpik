from django.urls import path

from .views import (
    MeView,
    SendOTPView,
    VerifyOTPView,
    SessionListView,
    SessionLogoutView,
    LogoutAllSessionsView,
    UserProfileView,
)
from .views import (
    AdminUserListView,
    AdminUserDetailView,
    AdminUserBanView,
    AdminUserUnbanView,
    DashboardView,
    AdminUserRoleUpdateView,
)
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [



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
    path(
        "profile/",
        UserProfileView.as_view()
    ),


    path(
        "admin/users/",
        AdminUserListView.as_view()
    ),


    path(
        "admin/users/<int:pk>/",
        AdminUserDetailView.as_view()
    ),


    path(
        "admin/users/<int:pk>/ban/",
        AdminUserBanView.as_view()
    ),


    path(
        "admin/users/<int:pk>/unban/",
        AdminUserUnbanView.as_view()
    ),
    path(
         "token/refresh/",
         TokenRefreshView.as_view(),
         name="token_refresh"
     ),
    path(
        "dashboard/",
        DashboardView.as_view()
    ),

    path(
        "admin/users/<int:pk>/role/",
        AdminUserRoleUpdateView.as_view()
    ),
]