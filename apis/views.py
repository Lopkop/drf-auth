from datetime import datetime

from django.contrib.auth.hashers import make_password
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import UserSerializer, TokenSerializer, UpdateUserSerializer
from .models import User, RefreshToken
from .services import generate_access_token, get_new_refresh_token, get_access_token_expiration_time, \
    decode_access_token, verify_password


@api_view(['POST'])
def sign_up(request):
    serializer = UserSerializer(data=request.data)
    if not serializer.is_valid() or len(request.data) > 2:
        return Response(status=422)
    if User.objects.filter(email=serializer.validated_data['email']).exists():
        return Response('User with this email already exists', status=400)

    user = User.objects.create(email=serializer.validated_data['email'],
                               password=make_password(serializer.validated_data['password']))
    user.save()

    return Response({'id': user.id, 'email': user.email}, status=200)


@api_view(['POST'])
def login(request):
    serializer = UserSerializer(data=request.data)
    if not serializer.is_valid() or len(request.data) > 2:
        return Response(status=422)

    try:
        user = User.objects.get(email=serializer.validated_data['email'])
        if not verify_password(serializer.validated_data['password'], user.password):
            return Response('Invalid password', status=400)
        refresh_token = RefreshToken.objects.get(user=user)
        refresh_token.delete()

        refresh_token = get_new_refresh_token(user)
    except User.DoesNotExist:
        return Response('User with this email does not exists', status=404)
    except RefreshToken.DoesNotExist:
        refresh_token = get_new_refresh_token(user)

    expiration_time = get_access_token_expiration_time()
    access_token = generate_access_token({'id': user.id, 'expires': str(expiration_time)})

    return Response({"access_token": access_token, "refresh_token": refresh_token.refresh_token}, status=200)


@api_view(['POST'])
def logout(request):
    serializer = TokenSerializer(data=request.data)
    if not serializer.is_valid() or len(request.data) > 1:
        return Response(status=422)
    token = RefreshToken.objects.get(refresh_token=serializer.validated_data.get('refresh_token'))
    token.delete()

    return Response({"success": "User logged out."}, status=200)


@api_view(['POST'])
def update_access_token(request):
    serializer = TokenSerializer(data=request.data)
    if not serializer.is_valid() or len(request.data) > 1:
        return Response(status=422)
    try:
        token = RefreshToken.objects.get(refresh_token=serializer.validated_data.get('refresh_token'))
        if token.expires < datetime.now(token.expires.tzinfo):
            return Response('Refresh token expired', status=400)
        access_token = generate_access_token({'id': token.user.id,
                                              'expires': str(get_access_token_expiration_time())})

        return Response({'access_token': access_token, 'refresh_token': token.refresh_token}, status=200)
    except RefreshToken.DoesNotExist:
        return Response('Invalid refresh token', status=400)


@api_view(['GET', 'PUT'])
def get_user(request):
    if not (token := request.headers.get('Authorization')):
        return Response('Access token was not provided', status=400)
    data = decode_access_token(token)
    if datetime.strptime(data.get('expires'), '%Y-%m-%d %H:%M:%S.%f') < datetime.now():
        return Response('Access token expired', status=400)

    try:
        user = User.objects.get(id=data.get('id'))
    except User.DoesNotExist:
        return Response('User not found', status=404)

    if request.method == 'PUT':
        print(request.data)
        serializer = UpdateUserSerializer(user, data=request.data)
        if (not serializer.is_valid()) or len(request.data) > 3 or not request.data:
            return Response(status=422)
        serializer.save()

        for key, value in serializer.validated_data.items():
            if key == 'username':
                user.name = value
            elif key == 'email':
                user.email = value
            elif key == 'password':
                user.password = make_password(value)
    return Response({'username': user.username,
                     'email': user.email,
                     'id': user.id}, status=200)
