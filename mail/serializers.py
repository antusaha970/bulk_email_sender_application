from rest_framework import serializers
from .models import *


class SMTPConfigurationSerializerForView(serializers.ModelSerializer):
    class Meta:
        model = SMTPConfiguration
        fields = ['id', 'name']


class SMTPConfigurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = SMTPConfiguration
        fields = "__all__"
        extra_kwargs = {
            'aws_access_key_id': {'required': True},
            'aws_secret_access_key': {'required': True},
            'host': {'required': True},
            'name': {'required': True},
        }

    def validate(self, attrs):
        name = attrs.get('name')
        user = self.context.get('user')

        is_exist = SMTPConfiguration.objects.filter(
            name=name, user=user).exists()
        if is_exist:
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
