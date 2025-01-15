from rest_framework import serializers
from .models import *

class SmsConfigurationSerializer(serializers.ModelSerializer):
    class Meta:
        model= SmsConfiguration
        fields="__all__"

class SmsConfigurationSerializerForview(serializers.ModelSerializer):
    class Meta:
        model= SmsConfiguration
        fields=["id","username","sender_number","user"]
       
    
class SmsComposeSerializer(serializers.ModelSerializer):
    class Meta:
        model=SmsCompose
        fields="__all__"

class SmsComposeSerializerForView(serializers.ModelSerializer):
    class Meta:
        model=SmsCompose
        fields=["id","sms_configuration","recipient_number"]


class RecipientsSerializer(serializers.ModelSerializer):
    class Meta:
        model=SmsRecipients
        fields="__all__"
        
class SandboxSerializer(serializers.ModelSerializer):
    class Meta:
        model=SandBox
        fields="__all__"
        