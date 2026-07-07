from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.conf import settings
from django.utils import timezone

from datetime import timedelta

from .managers import UserManager



class User(AbstractBaseUser, PermissionsMixin):

    ROLE_CHOICES = (
        ("student", "Student"),
        ("admin", "Admin"),
        ("support", "Support"),
        ("instructor", "Instructor"),
    )


    phone = models.CharField(
        max_length=15,
        unique=True
    )


    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default="student"
    )


    is_blocked = models.BooleanField(
        default=False
    )


    is_active = models.BooleanField(
        default=True
    )


    is_staff = models.BooleanField(
        default=False
    )


    created_at = models.DateTimeField(
        auto_now_add=True
    )


    updated_at = models.DateTimeField(
        auto_now=True
    )


    USERNAME_FIELD = "phone"


    objects = UserManager()


    def __str__(self):

        return self.phone





class OTPCode(models.Model):

    phone = models.CharField(
        max_length=15
    )


    code = models.CharField(
        max_length=6
    )


    is_used = models.BooleanField(
        default=False
    )


    expires_at = models.DateTimeField()


    created_at = models.DateTimeField(
        auto_now_add=True
    )


    def is_valid(self):

        return (
            not self.is_used
            and
            timezone.now() < self.expires_at
        )


    def __str__(self):

        return self.phone





class UserSession(models.Model):

    MAX_SESSIONS = 3


    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="sessions"
    )


    session_key = models.CharField(
        max_length=255,
        unique=True
    )


    device_name = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )


    ip_address = models.GenericIPAddressField(
        blank=True,
        null=True
    )


    user_agent = models.TextField(
        blank=True,
        null=True
    )


    is_active = models.BooleanField(
        default=True
    )


    created_at = models.DateTimeField(
        auto_now_add=True
    )


    last_activity = models.DateTimeField(
        auto_now=True
    )


    expires_at = models.DateTimeField()


    class Meta:

        ordering = [
            "-last_activity"
        ]



    def __str__(self):

        return f"{self.user.phone} - {self.device_name}"



    @classmethod
    def cleanup_old_sessions(cls, user):

        sessions = cls.objects.filter(
            user=user,
            is_active=True
        ).order_by(
            "last_activity"
        )


        if sessions.count() > cls.MAX_SESSIONS:

            extra = sessions.count() - cls.MAX_SESSIONS


            for session in sessions[:extra]:

                session.is_active = False

                session.save(
                    update_fields=[
                        "is_active"
                    ]
                )