from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
import os

# Create your views here.


@api_view(['GET'])
def healthcheck(request):
    """
    Endpoint de vérification de la santé de l'API
    Retourne le statut de l'application
    """
    return Response({
        'status': 'healthy',
        'message': 'API is running'
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
def version(request):
    """
    Endpoint qui retourne la version de l'application
    """
    app_version = os.getenv('APP_VERSION', '1.0.0')
    return Response({
        'version': app_version,
        'api': 'MediaProject2 API'
    }, status=status.HTTP_200_OK)
