from os import access
from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .Serializers import CreateuserSerializer, LoginSerializer
from .models import CustomUser
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from datetime import datetime


class CreateUserView(ModelViewSet):
    http_method_names =['post']
    queryset = CustomUser.objects.all()
    serializer_class = CreateuserSerializer
    
    def create(self, request):
        valid_request = self.serializer_class(data=request.data)
        valid_request.is_valid(raise_exception=True)
        
        
        CustomUser.objects.create(**valid_request.validated_data)
        return Response({"success":
            "user Created successfull"},status=status.HTTP_201_CREATED)
        
        
class LoginView(ModelViewSet):
    http_method_names = ["post"]
    queryset = CustomUser.objects.all()
    serializer_class = LoginSerializer

    def create(self, request):
        valid_request = self.serializer_class(data=request.data)
        valid_request.is_valid(raise_exception=True)
        
        #? accessing data in a dictionary
        new_user = valid_request.validated_data["is_new_user"]

        """ we use filter because it return an empty array if 
        it dosenot exists while get return an error if 
        doesnot extis"""
        if new_user:
            user = CustomUser.objects.filter(
                email=valid_request.validated_data["email"]
            )

            if user:
                user = user[0]
                if not user.password:
                    return Response({"user_id": user.id})
                else:
                    raise Exception("User has password already")
            else:
                raise Exception("User with email not found")

        user = authenticate(
            username=valid_request.validated_data["email"],
            password=valid_request.validated_data.get("password", None)
        )

        if not user:
            return Response(
                {"error": "Invalid email or password"},
                status=status.HTTP_400_BAD_REQUEST
            )
         
        #? the 1 means  the access token expires in 1 day
        access = get_access_token({"user_id": user.id}, 1)

        user.last_login = datetime.now()
        user.save()

        add_user_activity(user, "logged in")

        return Response({"access": access})
