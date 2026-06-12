from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import User

from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from .serializers import RegisterSerializer, AuthSerializer, ConfirmSerializer


@api_view(['POST'])
def registration_api_view(request):
    serializer = RegisterSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    username = serializer.validated_data['username']
    password = serializer.validated_data['password']

    user = User.objects.create_user(username=username,password=password,is_active=True)

    return Response(status=status.HTTP_201_CREATED,data={
            'user_id': user.id,
            'confirmation_code': user.confirmation_code
        })


@api_view(['POST'])
def confirm_api_view(request):
    serializer = ConfirmSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    username = serializer.validated_data['username']
    code = serializer.validated_data['code']

    try:
        user = User.objects.get(username=username,confirmation_code=code)
    except User.DoesNotExist:
        return Response({'error': 'Wrong code'},status=status.HTTP_400_BAD_REQUEST)

    user.is_active = True
    user.save()

    return Response({'message': 'User confirmed'})


@api_view(['POST'])
def authorization_api_view(request):
    serializer = AuthSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    username = serializer.validated_data['username']
    password = serializer.validated_data['password']

    user = authenticate(username=username,password=password)

    if user is not None:
        try:
            token = Token.objects.get(user=user)
        except Token.DoesNotExist:
            token = Token.objects.create(user=user)

        return Response(data={'key': token.key})

    return Response(status=status.HTTP_401_UNAUTHORIZED)