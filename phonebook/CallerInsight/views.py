# from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.response import Response

from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.decorators import permission_classes

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import *
from .serializers import *


#user registration
@permission_classes((AllowAny,))
class Register(APIView):
    def post(self, request):
        username = request.data.get("name")
        password = request.data.get("password")
        phone_number = request.data.get("phone_number")

        if not username or not phone_number or not password:
            return Response({
                "Error": "Name, phone_number, and password are required fields"
                },
                status = status.HTTP_400_BAD_REQUEST,
            )
        
        existing_user = UserProfile.objects.filter(phone_number=phone_number).first()
        if existing_user:
            return Response(
                {"Error": "User with this phone number already exists"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        email = request.data.get("email", "")

        user = User.objects.create_user(
            username=username,
            password=password,
            email=email,
        )

        profile = UserProfile.objects.create(
            user=user,
            phone_number=phone_number,
            email=email,
        )

        return Response(
            {"Message": "User registered successfully"},
            status=status.HTTP_200_OK,
        )
    

#user login
@permission_classes((AllowAny,))
class Login(APIView):
    def post(self, request):
        if not request.data:
            return Response({
                "Error": "username and password are required fields"
            },status=status.HTTP_400_BAD_REQUEST)
        
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response({
                "Error": "Invalid username or password",
            }, status=status.HTTP_404_NOT_FOUND)
        
        user = authenticate(username=username, password=password)
        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            "Token": token.key
        }, status=status.HTTP_200_OK) 



