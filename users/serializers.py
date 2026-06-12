from rest_framework import serializers


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class AuthSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class ConfirmSerializer(serializers.Serializer):
    username = serializers.CharField()
    code = serializers.CharField(max_length=6)