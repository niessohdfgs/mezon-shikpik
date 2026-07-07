from django.contrib.auth import get_user_model, authenticate

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from rest_framework_simplejwt.tokens import RefreshToken

import secrets

from .models import UserSession
from .serializers import (
    UserSerializer,
    UserSessionSerializer,
    RegisterSerializer,
    LoginSerializer,
)

from .services.otp import OTPService



User = get_user_model()




class RegisterView(APIView):

    def post(self, request):

        serializer = RegisterSerializer(
            data=request.data
        )


        serializer.is_valid(
            raise_exception=True
        )


        user = serializer.save()


        refresh = RefreshToken.for_user(
            user
        )


        return Response(
            {
                "user":
                    UserSerializer(user).data,

                "refresh":
                    str(refresh),

                "access":
                    str(
                        refresh.access_token
                    )
            }
        )






class LoginView(APIView):

    def post(self, request):

        serializer = LoginSerializer(
            data=request.data
        )


        serializer.is_valid(
            raise_exception=True
        )


        user = serializer.validated_data[
            "user"
        ]


        refresh = RefreshToken.for_user(
            user
        )


        return Response(
            {
                "user":
                    UserSerializer(user).data,

                "refresh":
                    str(refresh),

                "access":
                    str(
                        refresh.access_token
                    )
            }
        )







class SendOTPView(APIView):

    def post(self, request):

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


        return Response(
            OTPService.send_otp(phone)
        )








class VerifyOTPView(APIView):

    def post(self, request):

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



        if not OTPService.verify_otp(
            phone,
            code
        ):

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



        UserSession.cleanup_old_sessions(
            user
        )



        session = UserSession.objects.create(

            user=user,

            session_key=secrets.token_hex(
                32
            ),

            device_name=request.data.get(
                "device_name",
                "unknown"
            ),

            ip_address=request.META.get(
                "REMOTE_ADDR"
            ),

            user_agent=request.META.get(
                "HTTP_USER_AGENT"
            )
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








class MeView(APIView):

    permission_classes = [
        IsAuthenticated
    ]


    def get(self, request):

        return Response(
            UserSerializer(
                request.user
            ).data
        )








class SessionListView(APIView):

    permission_classes = [
        IsAuthenticated
    ]


    def get(self, request):

        sessions = UserSession.objects.filter(
            user=request.user,
            is_active=True
        )


        return Response(
            UserSessionSerializer(
                sessions,
                many=True
            ).data
        )








class SessionLogoutView(APIView):

    permission_classes = [
        IsAuthenticated
    ]


    def post(self, request):

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


    def post(self, request):

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