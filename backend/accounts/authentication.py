from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from django.utils import timezone

from .models import UserSession



class SessionAuthentication(BaseAuthentication):

    def authenticate(self, request):

        session_key = request.headers.get(
            "X-Session-Key"
        )


        if not session_key:
            return None


        try:

            session = (
                UserSession.objects
                .select_related("user")
                .get(
                    session_key=session_key
                )
            )


        except UserSession.DoesNotExist:

            raise AuthenticationFailed(
                "Invalid session"
            )


        if not session.is_active:

            raise AuthenticationFailed(
                "Session inactive"
            )


        if timezone.now() > session.expires_at:

            session.is_active = False

            session.save(
                update_fields=[
                    "is_active"
                ]
            )

            raise AuthenticationFailed(
                "Session expired"
            )


        user = session.user


        if user.is_blocked:

            raise AuthenticationFailed(
                "User blocked"
            )


        session.last_activity = timezone.now()

        session.save(
            update_fields=[
                "last_activity"
            ]
        )


        return (
            user,
            session
        )