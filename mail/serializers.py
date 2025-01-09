from rest_framework import serializers
from .models import *


class SMTPConfigurationSerializerForView(serializers.ModelSerializer):
    class Meta:
        model = SMTPConfiguration
        fields = ['id', 'username']


class SMTPConfigurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = SMTPConfiguration
        fields = ['username', 'password', 'host']
        extra_kwargs = {
            'username': {'required': True},
            'password': {'required': True},
            'host': {'required': True},
        }

    def validate(self, attrs):
        username = attrs.get('username')
        is_exist_username = SMTPConfiguration.objects.filter(
            username=username).exists()
        if is_exist_username:
            raise serializers.ValidationError(
                {"username": ["This username must be unique."]}, 400)
        return super().validate(attrs)


class EmailComposeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Email_Compose
        fields = "__all__"


class EmailComposeSerializerForView(serializers.ModelSerializer):
    class Meta:
        model = Email_Compose
        fields = ['id', 'subject']


class AttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attachment
        fields = "__all__"


class RecipientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipient
        fields = "__all__"


class OutboxSerializer(serializers.ModelSerializer):
    class Meta:
        model = Outbox
        fields = "__all__"
