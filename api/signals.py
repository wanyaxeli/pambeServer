from .models import User,Profile
from django.dispatch import receiver
from django.db.models.signals import post_save
@receiver(post_save,sender=User)
def createProfile(sender,instance,created,**kwargs):
    if created:
        profile=Profile.objects.create(user=instance)
        profile.save()