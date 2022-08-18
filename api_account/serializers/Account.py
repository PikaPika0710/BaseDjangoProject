from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from api_account.models import Account


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = '__all__'

    def save(self, **kwargs):
        validated_data = self.validated_data
        password = make_password(validated_data.get('password'))
        validated_data['password'] = password
        return super(AccountSerializer, self).save(**kwargs)


class UserAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'username', 'password', 'email']


class UserEditAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['username', "password"]

    def save(self, **kwargs):
        validated_data = self.validated_data
        password = make_password(validated_data.get('password'))
        validated_data['password'] = password
        return super(UserEditAccountSerializer, self).save(**kwargs)
