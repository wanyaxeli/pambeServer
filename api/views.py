from django.shortcuts import render
from .serializers import UserSerializers,ProfileSerializer,InterestsSerializer,CustomTokenObtainPairSerializer
from rest_framework.response import Response
from rest_framework import permissions 
from .models import User,Interests,Profile
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from decouple import config
from rest_framework_simplejwt.views import TokenObtainPairView
import jwt
# Create your views here.
class UserView(APIView):
    def post(self,request):
        data=request.data
        serializer=UserSerializers(data=data)
        if serializer.is_valid():
            user=serializer.save()
            email=user.email
            password=user.password
            SECRET_KEY =config('SECRET_KEY')
            accesstoken=RefreshToken.for_user(user).access_token
            refreshToken=RefreshToken.for_user(user)
            response_data = {
                'data': serializer.data,
                'access_token': str(accesstoken),
                'refresh_token': str(refreshToken),
            }
            return Response(response_data)
        else :
            return Response(serializer.errors)
    
    def get(self,request):
        user=request.user
        user=User.objects.all()
        serializer=UserSerializers(user,many=True)
        return Response(serializer.data)
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
class InterestsView(APIView):
    permission_classes=[permissions.IsAuthenticated]
    def post(self,request):
        data=request.data
        user=request.user
        serializer=InterestsSerializer(data=data)
        if serializer.is_valid():
            serializer.save(user=user)
            return Response(serializer.data)
        else :
            return Response(serializer.errors)
        
    def get(self,request,*args,**kwargs):
        pk=self.kwargs['pk']
        try:
            user=User.objects.get(pk=pk)
            interests=Interests.objects.get(user=user)
            serializer=InterestsSerializer(interests)
            return Response(serializer.data)
        except Interests.DoesNotExist:
            return Response('user does not exit')

class ProfileView(APIView):
    permission_classes=[permissions.IsAuthenticated]
    def get(self,request):
        user=request.user
        profile=Profile.objects.get(user=user)
        serializer=ProfileSerializer(profile)
        return serializer.data

class SpecificUserView(APIView):
    permission_classes=[permissions.IsAuthenticated]
    def get(self,request,*args,**kwargs):
        pk=self.kwargs['pk']
        user=User.objects.get(pk=pk)
        serializer=UserSerializers(user)
        return Response(serializer.data)