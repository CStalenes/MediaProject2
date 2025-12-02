from rest_framework import serializers


class PingSerializer(serializers.Serializer):
    message = serializers.CharField(default="pong")


class HealthCheckSerializer(serializers.Serializer):
    status = serializers.CharField(default="ok")


class VersionSerializer(serializers.Serializer):
    version = serializers.CharField(default="1.0.0")

