from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from cloudinary.models import CloudinaryField
from django.contrib.auth.models import BaseUserManager
# Create your models here.
user=settings.AUTH_USER_MODEL
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """
        Create and return a regular user with an email and password.
        """
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Create and return a superuser with an email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)
class User(AbstractUser):
    USERNAME_FIELD = 'email'
    phone_number=models.IntegerField(default=0)
    is_admin=models.BooleanField(default=False)
    email = models.EmailField(unique=True) # changes email to unique and blank to false
    REQUIRED_FIELDS = ['first_name','last_name'] # removes email from REQUIRED_FIELDS
    confirm_password=models.CharField(max_length=255,null=True)
    username = None  # Set username to None
    objects = CustomUserManager() 
    def __str__(self) -> str:
        return f'{self.first_name} {self.last_name}'
class ProfileImages(models.Model):
    user=models.ForeignKey(user,on_delete=models.CASCADE)
    image=CloudinaryField('image')
    def __str__(self) -> str:
        return self.user.first_name
class Profile(models.Model):
    user=models.OneToOneField(user,on_delete=models.CASCADE)
    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'
class Interests(models.Model):
    user=models.ForeignKey(user,on_delete=models.CASCADE)
    interest=models.JSONField()
    def __str__(self):
        return self.user.first_name
class Messages(models.Model):
    sender=models.ForeignKey(user,on_delete=models.CASCADE,related_name='sender')
    receipient=models.ForeignKey(user,on_delete=models.CASCADE,related_name='receipient')
    message=models.CharField(max_length=2000,default='',null=True)
    read=models.BooleanField(default=False,blank=True,null=True)
    def __str__(self) -> str:
        return f'{self.sender} {self.message}'
class Likes(models.Model):
    user=models.ForeignKey(user,on_delete=models.CASCADE,related_name='owner')
    myLikes=models.ManyToManyField(User)
   
    def __str__(self):
        return self.user.first_name 