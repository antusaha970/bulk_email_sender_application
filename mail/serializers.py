from rest_framework import serializers
from .models import *


class SMTPConfigurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = SMTPConfiguration
        fields = ['username', 'password', 'host']
        extra_kwargs = {
            'username': {'required': True},
            'password': {'required': True},
            'host': {'required': True},
        }


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
