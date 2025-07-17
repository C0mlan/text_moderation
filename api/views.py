from django.shortcuts import render
from rest_framework_api_key.permissions import HasAPIKey
from .serializer import RegistrationSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from .permissions import HasValidAPIKeyWithLimit
from .tasks import  predict_comment, predict_spam



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





@api_view(['GET'])
@permission_classes([HasValidAPIKeyWithLimit])
def test_view(request):
    return Response({"message": "You have access to the protected data!"}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([HasValidAPIKeyWithLimit])
def text_predict(request):
    text = request.data.get('text')
    toxic_result = predict_comment(text)
    spam_result = predict_spam(text)
 

    return Response({
    "toxicity_prediction": toxic_result,
    "spam_prediction": spam_result
     
    })


