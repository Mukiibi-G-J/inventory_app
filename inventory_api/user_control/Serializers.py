from user_control.models import UserActivities, CustomUser, Roles
from rest_framework import serializers


class CreateuserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    fullname = serializers.CharField()
    role = serializers.ChoiceField(Roles)


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(required=False)
    is_new_user = serializers.BooleanField(default=False, required=False)


class UpdatePasswordSerializer(serializers.Serializer):
    user_id = serializers.CharField()
    password = serializers.CharField()


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        exclude = ("password",)


class UserActivitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserActivities
        fieds = "__all__"
