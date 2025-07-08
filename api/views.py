from django.shortcuts import render
from rest_framework_api_key.permissions import HasAPIKey
from .serializer import RegistrationSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated



@api_view(['POST'])
@permission_classes([AllowAny])
def register_view(request):    
    serializer= RegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        response_data = {
            "response": "Account has been created.",
            "user" :serializer.data  
        }
        return Response(response_data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


