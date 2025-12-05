"""
Modèles Django ORM pour l'application media
Gestion des fichiers médias avec intégration ImageKit
Basé sur le MCD/MLD fourni
"""
import uuid
from django.db import models
from django.core.validators import MinValueValidator
from core.models import User


class Media(models.Model):
    """
    Modèle Media pour stocker les métadonnées des fichiers uploadés vers ImageKit
    Basé sur le MCD/MLD fourni
    """
    uuid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name='UUID'
    )
    uploader = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='uploaded_media',
        verbose_name='Uploader',
        help_text='Utilisateur qui a uploadé le fichier',
        db_column='uploader_id'  # Nom de colonne dans la DB
    )
    original_filename = models.CharField(
        max_length=255,  # Augmenté de 50 à 255 pour supporter les noms longs
        verbose_name='Nom de fichier original',
        help_text='Nom du fichier tel qu\'uploadé par l\'utilisateur'
    )
    file_size = models.IntegerField(
        validators=[MinValueValidator(0)],
        verbose_name='Taille du fichier (bytes)',
        help_text='Taille du fichier en octets'
    )
    mime_type = models.CharField(
        max_length=100,
        verbose_name='Type MIME',
        help_text='Type MIME du fichier (ex: image/jpeg, video/mp4)'
    )
    imagekit_file_id = models.CharField(
        max_length=255,
        unique=True,
        verbose_name='ImageKit File ID',
        help_text='ID unique du fichier dans ImageKit'
    )
    imagekit_url = models.URLField(
        max_length=500,  # Augmenté de 100 à 500 pour les URLs longues
        unique=True,
        verbose_name='ImageKit URL',
        help_text='URL publique du fichier sur ImageKit'
    )
    imagekit_thumbnail_url = models.URLField(
        max_length=500,  # Augmenté de 100 à 500 pour les URLs longues
        unique=True,
        blank=True,
        null=True,
        verbose_name='ImageKit Thumbnail URL',
        help_text='URL de la miniature du fichier sur ImageKit'
    )
    file_type = models.CharField(
        max_length=50,
        verbose_name='Type de fichier',
        help_text='Type de fichier (image, video, audio, document)'
    )
    duration_s = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name='Durée (secondes)',
        help_text='Durée du média en secondes (pour vidéos/audio)'
    )
    width = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name='Largeur (pixels)',
        help_text='Largeur du média en pixels (pour images/vidéos)'
    )
    height = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name='Hauteur (pixels)',
        help_text='Hauteur du média en pixels (pour images/vidéos)'
        # Note: corrigé "heigth" en "height"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Date de création'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Date de mise à jour'
    )
    
    class Meta:
        db_table = 'Media'
        verbose_name = 'Média'
        verbose_name_plural = 'Médias'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['uploader']),
            models.Index(fields=['file_type']),
            models.Index(fields=['created_at']),
            models.Index(fields=['imagekit_file_id']),
        ]
    
    def __str__(self):
        return f"{self.original_filename} ({self.file_type}) - {self.uploader.username}"


class MediaJob(models.Model):
    """
    Modèle MediaJob pour gérer les jobs de traitement de médias
    Exemples: conversion, génération de thumbnails, extraction de métadonnées
    """
    JOB_STATUS_CHOICES = [
        ('pending', 'En attente'),
        ('processing', 'En cours de traitement'),
        ('completed', 'Terminé'),
        ('failed', 'Échoué'),
        ('cancelled', 'Annulé'),
    ]
    
    JOB_TYPE_CHOICES = [
        ('thumbnail', 'Génération de miniature'),
        ('conversion', 'Conversion de format'),
        ('metadata', 'Extraction de métadonnées'),
        ('transcription', 'Transcription audio/vidéo'),
        ('compression', 'Compression'),
    ]
    
    uuid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name='UUID'
    )
    media = models.ForeignKey(
        Media,
        on_delete=models.CASCADE,
        related_name='jobs',
        verbose_name='Média',
        help_text='Média associé au job'
    )
    job_type = models.CharField(
        max_length=50,
        choices=JOB_TYPE_CHOICES,
        verbose_name='Type de job',
        help_text='Type de traitement à effectuer'
    )
    status = models.CharField(
        max_length=20,
        choices=JOB_STATUS_CHOICES,
        default='pending',
        verbose_name='Statut',
        help_text='Statut actuel du job'
    )
    started_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Date de début',
        help_text='Date de début du traitement'
    )
    completed_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Date de fin',
        help_text='Date de fin du traitement'
    )
    error_message = models.TextField(
        blank=True,
        null=True,
        verbose_name='Message d\'erreur',
        help_text='Message d\'erreur si le job a échoué'
    )
    result_data = models.JSONField(
        default=dict,
        blank=True,
        verbose_name='Données de résultat',
        help_text='Données JSON contenant les résultats du job'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Date de création'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Date de mise à jour'
    )
    
    class Meta:
        db_table = 'MediaJobs'
        verbose_name = 'Job média'
        verbose_name_plural = 'Jobs médias'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['media']),
            models.Index(fields=['status']),
            models.Index(fields=['job_type']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"{self.get_job_type_display()} - {self.media.original_filename} ({self.get_status_display()})"
    
    def mark_as_processing(self):
        """Marquer le job comme en cours de traitement"""
        from django.utils import timezone
        self.status = 'processing'
        self.started_at = timezone.now()
        self.save()
    
    def mark_as_completed(self, result_data=None):
        """Marquer le job comme terminé"""
        from django.utils import timezone
        self.status = 'completed'
        self.completed_at = timezone.now()
        if result_data:
            self.result_data = result_data
        self.save()
    
    def mark_as_failed(self, error_message):
        """Marquer le job comme échoué"""
        from django.utils import timezone
        self.status = 'failed'
        self.completed_at = timezone.now()
        self.error_message = error_message
        self.save()
