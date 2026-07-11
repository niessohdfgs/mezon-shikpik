from django.contrib.auth import authenticate, get_user_model

from rest_framework import serializers

from rest_framework_simplejwt.tokens import RefreshToken

from .models import UserSession


User = get_user_model()



class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        write_only=True,
        min_length=6
    )


    confirm_password = serializers.CharField(
        write_only=True
    )


    class Meta:

        model = User

        fields = [
            "phone",
            "password",
            "confirm_password",
        ]



    def validate(self, data):

        if data["password"] != data["confirm_password"]:

            raise serializers.ValidationError(
                {
                    "password":
                    "Passwords do not match"
                }
            )


        if User.objects.filter(
            phone=data["phone"]
        ).exists():

            raise serializers.ValidationError(
                {
                    "phone":
                    "User already exists"
                }
            )


        return data



    def create(self, validated_data):

        validated_data.pop(
            "confirm_password"
        )


        user = User.objects.create_user(
            **validated_data
        )


        return user





class LoginSerializer(serializers.Serializer):

    phone = serializers.CharField()


    password = serializers.CharField(
        write_only=True
    )


    def validate(self, data):

        user = authenticate(
            phone=data["phone"],
            password=data["password"]
        )


        if not user:

            raise serializers.ValidationError(
                "Invalid phone or password"
            )


        if user.is_blocked:

            raise serializers.ValidationError(
                "User blocked"
            )


        data["user"] = user


        return data





class UserSerializer(serializers.ModelSerializer):


    class Meta:

        model = User

        fields = [
            "id",
            "phone",
            "role",
            "is_staff",
            "is_superuser",
            "is_blocked",
        ]





class UserSessionSerializer(serializers.ModelSerializer):


    class Meta:

        model = UserSession

        fields = [
            "id",
            "device_name",
            "ip_address",
            "user_agent",
            "created_at",
            "last_activity",
            "is_active",
        ]





class TokenSerializer(serializers.Serializer):

    access = serializers.CharField()

    refresh = serializers.CharField()


    @staticmethod
    def get_tokens(user):

        refresh = RefreshToken.for_user(
            user
        )


        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token)
        }
    

class UserProfileSerializer(serializers.ModelSerializer):


    class Meta:

        model = User

        fields = [
            "id",
            "phone",
            "role",
            "is_blocked",
            "created_at",
            "updated_at",
        ]


        read_only_fields = [
            "id",
            "phone",
            "role",
            "is_blocked",
            "created_at",
            "updated_at",
        ]


class AdminUserSerializer(serializers.ModelSerializer):


    class Meta:

        model = User

        fields = [
            "id",
            "phone",
            "role",
            "is_blocked",
            "is_active",
            "is_staff",
            "created_at",
            "updated_at",
        ]


        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]