import logging

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes

from media.services.imagekit_service import ImageKitUploadService

logger = logging.getLogger(__name__)


# ============ FILE UPLOAD ENDPOINTS ============

class UploadFileView(APIView):
    """
    Vue pour uploader un fichier vers ImageKit.
    """
    
    parser_classes = (MultiPartParser,)
    
    @extend_schema(
        summary="Upload file to ImageKit.io",
        description="""
        Upload un fichier (image, document, etc.) vers ImageKit via cette API Django.
        
        **Architecture:**
        - Client → `POST http://localhost:8055/api/files/upload/` (cette API Django)
        - API Django → `https://upload.imagekit.io/api/v1/files/upload` (ImageKit API, interne)
        
        **Instructions pour Swagger UI:**
        1. Cliquez sur "Try it out"
        2. Cliquez sur "Choose File" dans le champ "file"
        3. Sélectionnez votre fichier (max 10MB)
        4. Cliquez sur "Execute"
        
        Le fichier sera uploadé vers ImageKit (via l'API interne) et vous recevrez l'URL publique.
        
        **Note:** L'URL ImageKit (`https://upload.imagekit.io/api/v1/files/upload`) est utilisée en interne
        par le service. Vous n'avez pas besoin de l'appeler directement.
        """,
        tags=["upload"],
        request={
            "multipart/form-data": {
                "type": "object",
                "properties": {
                    "file": {
                        "type": "string",
                        "format": "binary",
                        "description": "Fichier à uploader (image, document, etc.) - Max 10MB"
                    }
                },
                "required": ["file"]
            }
        },
        responses={
            200: {
                "description": "Upload réussi",
                "content": {
                    "application/json": {
                        "example": {
                            "success": True,
                            "fileId": "67890abcdef1234567890",
                            "name": "unique-name-abc123.jpg",
                            "size": 125000,
                            "filePath": "/uploads/unique-name-abc123.jpg",
                            "url": "https://ik.imagekit.io/votre-endpoint/uploads/unique-name-abc123.jpg",
                            "fileType": "image",
                            "height": 400,
                            "width": 600
                        }
                    }
                }
            },
            400: {
                "description": "Erreur de validation",
                "content": {
                    "application/json": {
                        "example": {
                            "error": "No file uploaded"
                        }
                    }
                }
            },
            500: {
                "description": "Erreur serveur",
                "content": {
                    "application/json": {
                        "example": {
                            "error": "Upload failed: [message d'erreur]",
                            "details": "Détails supplémentaires"
                        }
                    }
                }
            }
        },
        examples=[
            OpenApiExample(
                "Upload réussi",
                value={
                    "success": True,
                    "fileId": "67890abcdef1234567890",
                    "name": "unique-name-abc123.jpg",
                    "url": "https://ik.imagekit.io/votre-endpoint/uploads/unique-name-abc123.jpg",
                    "size": 125000,
                    "filePath": "/uploads/unique-name-abc123.jpg",
                    "fileType": "image"
                }
            )
        ]
    )
    def post(self, request):
        incoming_file = request.FILES.get("file")
        
        if incoming_file is None:
            return Response({"error": "No file uploaded"}, status=400)
        
        # Valider la taille du fichier (max 10MB)
        max_size = 10 * 1024 * 1024  # 10MB
        if incoming_file.size > max_size:
            return Response({
                "error": f"File too large. Maximum size: 10MB, got: {incoming_file.size / (1024*1024):.2f}MB"
            }, status=400)
        
        # Vérifier que le fichier n'est pas vide
        if incoming_file.size == 0:
            return Response({"error": "File is empty"}, status=400)
        
        try:
            imagekit_service = ImageKitUploadService()
            result = imagekit_service.upload_file(
                file_obj=incoming_file,
                file_name=None,  # Utilise le nom du fichier automatiquement
                unique_name=True,  # Génère un nom unique
                folder='/uploads',
            )
            
            # Retourner le résultat d'ImageKit (déjà au format JSON)
            # La méthode upload_file lève ValueError en cas d'erreur, donc si on arrive ici, c'est un succès
            return Response(result, status=200)
            
        except ValueError as e:
            # Erreur ImageKit (403, 500, etc.) ou configuration
            logger.error(f"ImageKit error: {e}")
            return Response({"error": str(e)}, status=500)
        except Exception as exc:
            logger.error(f"Upload failed: {exc}", exc_info=True)
            return Response({"error": str(exc)}, status=500)

# Create your views here.
