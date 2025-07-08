from django.db import models

from rest_framework_api_key.models import AbstractAPIKey
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone


class MyAPIKey(AbstractAPIKey):
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    user_key = models.CharField(max_length=128, blank=True, null=True)

        
    usage_limit = models.PositiveIntegerField(default=5)  
    usage_count = models.PositiveIntegerField(default=0)     
    blocked = models.BooleanField(default=False)            
    expires_at = models.DateTimeField(null=True, blank=True) 

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    
    def is_valid(self):
        if self.blocked:
            return False
        if self.expires_at and timezone.now() > self.expires_at:
            return False
        return self.usage_count < self.usage_limit

    def __str__(self):
        return f"APIKey({self.user.username}, {self.prefix})"   
    
         
def create_key(sender, instance, created, **kwargs):
    if created:
        api_key_obj, key = MyAPIKey.objects.create_key(name=instance.username, user=instance)
        api_key_obj.user_key = key  
        api_key_obj.save()
        print(f"API Key for {instance.username}: {key}")

post_save.connect(create_key, sender=User)
 
