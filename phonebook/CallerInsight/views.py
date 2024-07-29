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


#Searching user by name  
class SearchByName(APIView):
    def get(self, request):
        name = request.data.get("name")
        if not name:
            return Response({
                "Error": "Name is required"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        name_filter = UserProfile.objects.filter(user__username__startswith = name) | UserProfile.objects.filter(user__username__contains = name)
        contact_filter = Contact.objects.filter(name__startswith = name) | Contact.objects.filter(name__contains = name)
        
        response = []

        print("name_filter:", name_filter)

        for profile in name_filter:
            response.append({
                "name": profile.user.username,
                "phone_number": profile.phone_number,
                "spam": profile.spam
            })

        for profile in contact_filter:
            response.append({
                "name": profile.name,
                "phone_number": profile.phone_number,
                "spam": profile.spam
            })

        return Response({
                "data": response
            },
            status= status.HTTP_200_OK
        )

#Searching user by phone number
class SearchByPhoneNumber(APIView):
    def get(self, request):
        phone_number = request.data.get("phone_number")
        if not phone_number:
            return Response({
                "Error": "Phone number is required"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        profile = UserProfile.objects.filter(phone_number=phone_number).first()
        print(profile)

        if profile:
            # user = User.objects.filter(username = profile.user.username, is_active = True)
            # print("user:",user)
            return Response({
                "name": profile.user.username,
                "phone_number":profile.phone_number,
                "spam":profile.spam,
                "email":profile.email
            }, status=status.HTTP_200_OK)
        else:
            contact = Contact.objects.filter(phone_number=phone_number)
            serializer=ContactSerializer(contact,many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)

#Marking a user as spam 
class MarkSpam(APIView):
    def post(self, request):
        phone_number = request.data.get("phone_number")
        if not phone_number:
            return Response(
				{
					"Error":"Phone number required!!"
				},
				status = status.HTTP_400_BAD_REQUEST
			)
        contact, _ = Contact.objects.get_or_create(phone_number=phone_number)
        profile, _ = UserProfile.objects.get_or_create(phone_number=phone_number)

        contact.spam = True
        profile.spam = True
        contact.save()
        profile.save()

        return Response(
            {"Message": "Contact marked as spam successfully"},
            status=status.HTTP_200_OK,
        )

