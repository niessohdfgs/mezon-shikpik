from django.contrib.auth import get_user_model
from django.utils import timezone

from datetime import timedelta

import secrets


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


from rest_framework_simplejwt.tokens import RefreshToken


from .models import UserSession

from .serializers import UserSerializer

from .services.otp import OTPService
from .serializers import UserProfileSerializer
from rest_framework.generics import RetrieveUpdateAPIView  

from rest_framework.generics import (
    ListAPIView,
    RetrieveUpdateDestroyAPIView,
)

from .permissions import IsAdmin

from .serializers import AdminUserSerializer



User = get_user_model()





class SendOTPView(APIView):

    def post(
        self,
        request
    ):

        phone = request.data.get(
            "phone"
        )


        if not phone:

            return Response(
                {
                    "error":
                    "Phone is required"
                },
                status=400
            )



        result = OTPService.send_otp(
            phone
        )


        return Response(
            result
        )








class VerifyOTPView(APIView):

    def post(
        self,
        request
    ):


        phone = request.data.get(
            "phone"
        )


        code = request.data.get(
            "code"
        )



        if not phone or not code:

            return Response(
                {
                    "error":
                    "Phone and code required"
                },
                status=400
            )



        is_valid = OTPService.verify_otp(
            phone,
            code
        )



        if not is_valid:

            return Response(
                {
                    "error":
                    "Invalid OTP"
                },
                status=400
            )




        user, created = User.objects.get_or_create(

            phone=phone,

            defaults={
                "role": "student"
            }

        )




        if user.is_blocked:

            return Response(
                {
                    "error":
                    "User blocked"
                },
                status=403
            )





        session_key = secrets.token_hex(32)




        UserSession.cleanup_old_sessions(
            user
        )



        session = UserSession.objects.create(

            user=user,

            session_key=session_key,


            device_name=request.data.get(
                "device_name",
                "unknown"
            ),


            ip_address=request.META.get(
                "REMOTE_ADDR"
            ),


            user_agent=request.META.get(
                "HTTP_USER_AGENT"
            ),


            expires_at=timezone.now()
            +
            timedelta(days=7)

        )





        refresh = RefreshToken.for_user(
            user
        )





        return Response(

            {

                "user":
                    UserSerializer(user).data,


                "session":
                    session.session_key,


                "expires_at":
                    session.expires_at,


                "refresh":
                    str(refresh),


                "access":
                    str(
                        refresh.access_token
                    )

            }

        )









class LogoutView(APIView):

    permission_classes = [
        IsAuthenticated
    ]


    def post(
        self,
        request
    ):


        session_key = request.data.get(
            "session"
        )


        UserSession.objects.filter(

            session_key=session_key,

            user=request.user

        ).update(

            is_active=False

        )


        return Response(
            {
                "message":
                "Logged out"
            }
        )









class MeView(APIView):

    permission_classes = [
        IsAuthenticated
    ]


    def get(
        self,
        request
    ):


        return Response(
            UserSerializer(
                request.user
            ).data
        )









class SessionListView(APIView):

    permission_classes = [
        IsAuthenticated
    ]


    def get(
        self,
        request
    ):


        sessions = UserSession.objects.filter(

            user=request.user,

            is_active=True

        )



        return Response(
            [
                {
                    "id": s.id,
                    "device_name": s.device_name,
                    "ip_address": s.ip_address,
                    "user_agent": s.user_agent,
                    "created_at": s.created_at,
                    "last_activity": s.last_activity,
                    "expires_at": s.expires_at
                }

                for s in sessions
            ]
        )









class SessionLogoutView(APIView):

    permission_classes = [
        IsAuthenticated
    ]


    def post(
        self,
        request
    ):


        session_id = request.data.get(
            "session_id"
        )


        UserSession.objects.filter(

            id=session_id,

            user=request.user

        ).update(

            is_active=False

        )


        return Response(
            {
                "message":
                "Session logged out"
            }
        )









class LogoutAllSessionsView(APIView):

    permission_classes = [
        IsAuthenticated
    ]


    def post(
        self,
        request
    ):


        UserSession.objects.filter(

            user=request.user

        ).update(

            is_active=False

        )


        return Response(
            {
                "message":
                "All sessions logged out"
            }
        )
    

from django.contrib.auth import authenticate


class RegisterView(APIView):

    def post(self, request):

        phone = request.data.get("phone")
        password = request.data.get("password")

        if not phone or not password:
            return Response(
                {
                    "error": "phone and password required"
                },
                status=400
            )


        if User.objects.filter(phone=phone).exists():

            return Response(
                {
                    "error": "User already exists"
                },
                status=400
            )


        user = User.objects.create_user(
            phone=phone,
            password=password,
            role="student"
        )


        refresh = RefreshToken.for_user(user)


        return Response(
            {
                "user": UserSerializer(user).data,
                "refresh": str(refresh),
                "access": str(refresh.access_token)
            },
            status=201
        )





class LoginView(APIView):

    def post(self, request):

        phone = request.data.get("phone")
        password = request.data.get("password")


        user = authenticate(
            phone=phone,
            password=password
        )


        if not user:

            return Response(
                {
                    "error": "Invalid credentials"
                },
                status=400
            )


        refresh = RefreshToken.for_user(user)


        return Response(
            {
                "user": UserSerializer(user).data,
                "refresh": str(refresh),
                "access": str(refresh.access_token)
            }
        )
    
class UserProfileView(RetrieveUpdateAPIView):

    serializer_class = UserProfileSerializer

    permission_classes = [
        IsAuthenticated
    ]


    def get_object(self):

        return self.request.user



# =========================
# Admin Users
# =========================


class AdminUserListView(ListAPIView):

    serializer_class = AdminUserSerializer

    permission_classes = [
        IsAuthenticated,
        IsAdmin
    ]


    queryset = User.objects.all().order_by(
        "-id"
    )





class AdminUserDetailView(
    RetrieveUpdateDestroyAPIView
):

    serializer_class = AdminUserSerializer

    permission_classes = [
        IsAuthenticated,
        IsAdmin
    ]


    queryset = User.objects.all()







class AdminUserBanView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsAdmin
    ]


    def post(
        self,
        request,
        pk
    ):

        user = User.objects.get(
            id=pk
        )


        user.is_blocked = True

        user.save()



        return Response(
            {
                "message":
                "User banned"
            }
        )








class AdminUserUnbanView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsAdmin
    ]


    def post(
        self,
        request,
        pk
    ):


        user = User.objects.get(
            id=pk
        )


        user.is_blocked = False

        user.save()



        return Response(
            {
                "message":
                "User unbanned"
            }
        )