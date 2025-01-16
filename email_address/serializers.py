from rest_framework import serializers


class EmailAddressListSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
