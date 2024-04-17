from rest_framework import serializers

from .models import User, RefreshToken


class UserSerializer(serializers.HyperlinkedModelSerializer):
    def validate(self, data):
        if not data.get('username'):
            data['username'] = ''
        return data

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {'email': {'required': True}, 'password': {'required': True}}


class UpdateUserSerializer(serializers.HyperlinkedModelSerializer):
    def validate(self, data):
        if not (data.get('username') or data.get('email') or data.get('password')):
            return False
        return data

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {'email': {'required': False}, 'password': {'required': False},
                         'username': {'required': False}}


class TokenSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = RefreshToken
        fields = ['refresh_token']
        extra_kwargs = {'refresh_token': {'required': True}}
