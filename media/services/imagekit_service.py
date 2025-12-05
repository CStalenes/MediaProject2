"""
Service pour uploader des fichiers à ImageKit.
Documentation: https://imagekit.io/docs/api-reference/upload-file/upload-file
"""

import requests
import os
import base64
from typing import Dict, Optional, BinaryIO
from django.conf import settings


class ImageKitUploadService:
    """Service centralisé pour uploader des fichiers à ImageKit"""
    
    # Endpoints ImageKit
    # Documentation: https://imagekit.io/docs/api-reference/upload-file/upload-file
    # IMPORTANT: Utiliser /api/v1/files/upload (pas v2) pour l'upload avec Basic Auth
    UPLOAD_URL = 'https://upload.imagekit.io/api/v1/files/upload'  # ✅ URL officielle ImageKit
    API_BASE_URL = 'https://api.imagekit.io/v1'
    
    # URL pour l'upload (utiliser v1, pas v2)
    IMAGEKIT_API_URL = 'https://upload.imagekit.io/api/v1/files/upload'
    
    #IMAGEKIT_URL_ENDPOINT = os.getenv('IMAGEKIT_URL_ENDPOINT') or getattr(settings, 'IMAGEKIT_URL_ENDPOINT', None)

    def __init__(self):
        """Initialiser le service avec les credentials ImageKit"""
        self.api_key = os.getenv('IMAGEKIT_API_KEY') or getattr(settings, 'IMAGEKIT_API_KEY', None)
        self.public_key = os.getenv('IMAGEKIT_PUBLIC_KEY') or getattr(settings, 'IMAGEKIT_PUBLIC_KEY', None)
        self.url_endpoint = os.getenv('IMAGEKIT_URL_ENDPOINT') or getattr(settings, 'IMAGEKIT_URL_ENDPOINT', None)
        
        if not self.api_key or not self.public_key:
            raise ValueError(
                "ImageKit credentials non configurées. "
                "Définissez IMAGEKIT_API_KEY et IMAGEKIT_PUBLIC_KEY dans les variables d'environnement ou settings.py"
            )
    
    
    
    def upload_file(
        self,
        file_obj: BinaryIO,
        file_name: Optional[str] = None,
        unique_name: bool = False,
        folder: Optional[str] = None,
        tags: Optional[list] = None,
    ) -> Dict:
        """
        Upload any file to ImageKit using REST API + Basic Auth (base64).
        Returns ImageKit JSON response as dict.
        
        Args:
            file_obj: Objet fichier (request.FILES['file'])
            file_name: Nom du fichier (optionnel, utilise file_obj.name si non fourni)
            unique_name: Si True, ImageKit génère un nom unique
            folder: Dossier de destination (optionnel)
            tags: Liste de tags (optionnel)
        """
        # Utiliser le nom du fichier si non fourni
        if not file_name:
            file_name = getattr(file_obj, 'name', 'uploaded_file')
        
        # S'assurer que le fichier est lu depuis le début
        if hasattr(file_obj, 'seek'):
            file_obj.seek(0)
        
        # Préparer l'authentification Basic Auth
        private_key = self.api_key
        token = base64.b64encode(f"{private_key}:".encode()).decode()
        headers = {"Authorization": f"Basic {token}"}
        
        # Préparer les fichiers
        content_type = getattr(file_obj, 'content_type', None)
        files = {
            "file": (file_name, file_obj, content_type) if content_type else (file_name, file_obj)
        }
        
        # Préparer le payload
        payload = {
            "fileName": file_name,
            "useUniqueFileName": str(unique_name).lower()
        }
        
        if folder:
            payload["folder"] = folder
        if tags:
            payload["tags"] = ','.join(tags) if isinstance(tags, list) else tags
        
        # Faire la requête
        response = requests.post(
            self.IMAGEKIT_API_URL,
            files=files,
            data=payload,
            headers=headers,
            timeout=60
        )
        
        # Vérifier le statut
        if response.status_code != 200:
            raise ValueError(f"ImageKit error: {response.text}")
        
        return response.json()
    

    def list_files(self, folder: Optional[str] = None, limit: int = 100, skip: int = 0) -> Dict:
        """
        Lister les fichiers.
        
        Args:
            folder: Dossier à lister (optionnel)
            limit: Nombre max de fichiers
            skip: Nombre de fichiers à sauter
            
        Returns:
            Dict avec la liste des fichiers
        """
        try:
            url = f"{self.API_BASE_URL}/files"
            
            params = {
                'limit': limit,
                'skip': skip,
            }
            
            if folder:
                params['searchQuery'] = f"folder = '{folder}'"
            
            response = requests.get(
                url,
                params=params,
                auth=(self.api_key, ''),
                timeout=30,
            )
            
            if response.status_code == 200:
                return {
                    'success': True,
                    'data': response.json(),
                }
            
            return {
                'success': False,
                'status_code': response.status_code,
                'error': response.text,
            }
        
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
            }

