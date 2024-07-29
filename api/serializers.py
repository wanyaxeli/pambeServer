from rest_framework import serializers
from django.conf import settings
from .models import User,Interests,Profile,ProfileImages,Likes,Messages
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
# user=settings.AUTH_USER_MODEL
class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model=User
        fields='__all__'
    def validate(self, data):
        password = data.get('password')
        confirm_password = data.get('confirm_password')

        if password != confirm_password:
            raise serializers.ValidationError({'error': 'Password do not match'})

        # Remove the confirm_password field from the validated data
        del data['confirm_password']

        # Hash the password before saving it
        data['password'] = make_password(password)

        return data 


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
   def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['email'] = user.email
        token['first_name'] = user.first_name
        # ...

        return token
class InterestsSerializer(serializers.ModelSerializer):
    class Meta:
        model=Interests
        fields='__all__'
        extra_kwargs = {'user': {'required': False}} 

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=Profile
        fields='__all__'          

# class MessageSerializer(serializers.ModelSerializer):
#     class Meta:
#         model=Messages
#         fields='__all__'        