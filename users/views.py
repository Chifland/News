from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth import authenticate
from users.serializers import AuthorizationValidateSerializer, RegistrationVlidateSerializer
from django.contrib.auth.models import User


@api_view(['POST'])
def registration_api_view(request):
    serializer = RegistrationVlidateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    username = serializer.validated_data.get('username')
    password = serializer.validated_data.get('password')

    user = User.objects.create_user(username=username, password=password)
    return Response(status=201, data={"user_id": user.id})

@api_view(['POST'])
def authorization_api_view(request):
    # 0. Step: Validation
    serializer = AuthorizationValidateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    # 1. Step: Get data from client
    username = serializer.validated_data.get('username')
    password = serializer.validated_data.get('password')

    # 2. Step: Search user by credentials
    user = authenticate(username=username, password=password)
    # user = authenticate(**serializer.validated_data)

    # 3. Step: Return Key
    if user:
        token_, created = Token.objects.get_or_create(user=user)
        return Response(data={"key": token_.key})
    # 4. Step: Return Error
    return Response(status=401, data={'message': 'User not found'})

