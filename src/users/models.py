from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from .utils import generate_avatar, save_avatar_to_file
import os

# We'll use Django's built-in User model, so no custom models needed here 

class User(AbstractUser):
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    
    def get_avatar_url(self):
        if self.avatar:
            return self.avatar.url
        return None

@receiver(post_save, sender=User)
def create_user_avatar(sender, instance, created, **kwargs):
    """
    Signal handler to create an avatar when a new user is created
    """
    if created and not instance.avatar:
        # Generate avatar with size 200
        avatar_image = generate_avatar(avatar_size=200, nickname=instance.username)
        
        # Create filename
        filename = f"avatar_{instance.username}.png"
        
        # Save avatar
        instance.avatar = save_avatar_to_file(avatar_image, filename)
        instance.save() 