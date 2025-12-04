from rest_framework.views import APIView
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema

from .serializers import (
    PingSerializer, 
    HealthCheckSerializer, 
    VersionSerializer,
)

# ============ CORE ENDPOINTS ============

class HealthCheckView(APIView):
    @extend_schema(
        summary="Health check",
        description="Check if the API is alive.",
        responses={200: HealthCheckSerializer},
        tags=["core"],
    )
    def get(self, request):
        return Response({"status": "ok"})


class VersionView(APIView):
    @extend_schema(
        summary="API version",
        description="Return the current version of the API.",
        responses={200: VersionSerializer},
        tags=["core"],
    )
    def get(self, request):
        return Response({"version": "1.0.0"})


class PingView(APIView):
    @extend_schema(
        summary="Ping",
        description="Utility endpoint to check responses",
        responses={200: PingSerializer},
        tags=["core"],
    )
    def get(self, request):
        return Response({"message": "pong"}, status=status.HTTP_200_OK)

