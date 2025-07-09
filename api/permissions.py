from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied
from .models import MyAPIKey
from django.dispatch import receiver
from django.utils import timezone


#Custom permission class that validates an API key from the request header.
class HasValidAPIKeyWithLimit(BasePermission):

    def has_permission(self, request, view):
        key = request.headers.get("Authorization", "").replace("Api-Key ", "").strip()

        if not key:
            raise PermissionDenied("API key not provided.")

        try:
            api_key = MyAPIKey.objects.get(user_key=key)

            if api_key.blocked:
                raise PermissionDenied("API key is blocked.")

            if api_key.expires_at and timezone.now() > api_key.expires_at:
                raise PermissionDenied("API key has expired.")

            if api_key.usage_limit is not None and api_key.usage_count >= api_key.usage_limit:
                raise PermissionDenied("API key usage limit reached.")

            
            api_key.usage_count += 1
            api_key.save()

            return True

        except MyAPIKey.DoesNotExist:
            raise PermissionDenied("Authentication credentials were not provided.")