from rest_framework import serializers
from django.contrib.auth.models import User


class AccountSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = User
        fields = ['username',
                  'password']
        extra_kwargs = {
            'username': {'required': True},
            'password': {'required': True},
        }

    def validate(self, attrs):
        username = attrs.get('username')

        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError(
                "A user with that username already exists")

        return super().validate(attrs)

    def save(self, **kwargs):
        username = self.validated_data['username']
        password = self.validated_data['password']

        account = User(username=username)

        account.set_password(password)
        account.is_active = True

        account.save()
        return account


class AccountLoginSerializer(serializers.Serializer):
    password = serializers.CharField(required=True, write_only=True)
    username = serializers.CharField(required=True, write_only=True)
