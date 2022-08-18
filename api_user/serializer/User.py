from django.db import transaction
from rest_framework import serializers

from api_account.serializers import UserAccountSerializer
from api_user.models import User


class RegisterUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class DetailUserSerializer(serializers.ModelSerializer):
    account = UserAccountSerializer()

    class Meta:
        model = User
        fields = ['name', 'phone', 'birthday', 'gender', 'career', 'account']


class UpdateUserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name', 'phone', 'birthday', 'gender', 'career']

    @transaction.atomic
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)
