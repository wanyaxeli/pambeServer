from django.contrib import admin
from .models import User,Messages,Likes,ProfileImages,Interests,Profile
# Register your models here.
admin.site.register(User)
admin.site.register(Messages)
admin.site.register(Likes)
admin.site.register(ProfileImages)
admin.site.register(Interests)
admin.site.register(Profile)