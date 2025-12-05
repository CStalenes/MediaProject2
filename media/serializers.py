"""
Serializers pour l'upload et la gestion des fichiers avec ImageKit.
Référence: https://www.django-rest-framework.org/api-guide/serializers/
"""

from rest_framework import serializers


# ============ UPLOAD SERIALIZERS ============

class UploadFileSerializer(serializers.Serializer):
    """
    Serializer pour l'upload de fichier vers ImageKit.
    Accepte uniquement le fichier (file). Les autres paramètres sont gérés automatiquement.
    """
    file = serializers.FileField(required=True)

    def validate_file(self, file):
        """Valider le fichier"""
        if not file:
            raise serializers.ValidationError("Aucun fichier fourni")
        
        if file.size == 0:
            raise serializers.ValidationError("Le fichier est vide")
        
        # Max 10MB
        max_size = 10 * 1024 * 1024
        if file.size > max_size:
            raise serializers.ValidationError(
                f"Fichier trop volumineux ({file.size / (1024*1024):.2f}MB). Max: 10MB"
            )
        
        return file



class ErrorResponseSerializer(serializers.Serializer):
    """
    Serializer pour les réponses d'erreur.
    """
    
    success = serializers.BooleanField(default=False)
    error = serializers.CharField(help_text="Message d'erreur")
    message = serializers.CharField(required=False, help_text="Message supplémentaire")
    errors = serializers.DictField(required=False, help_text="Détail des erreurs de validation")

