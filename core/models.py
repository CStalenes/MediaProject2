"""
Modèles Django ORM pour l'application core
Gestion des utilisateurs et rôles
"""
import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.utils import timezone

    
class User(AbstractBaseUser):
    """
    Modèle User personnalisé basé sur le MCD/MLD fourni
    Utilise UUID comme clé primaire au lieu de l'ID auto-incrémenté
    """
    uuid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name='UUID'
    )
    email = models.EmailField(
        max_length=50,
        unique=True,
        verbose_name='Email',
        help_text='Adresse email de l\'utilisateur'
    )
    username = models.CharField(
        max_length=50,
        unique=True,
        verbose_name='Nom d\'utilisateur',
        help_text='Nom d\'utilisateur unique'
    )
    # password est hérité de AbstractBaseUser
    is_active = models.BooleanField(
        default=True,
        verbose_name='Actif',
        help_text='Indique si l\'utilisateur est actif'
    )
    is_admin = models.BooleanField(
        default=False,
        verbose_name='Administrateur',
        help_text='Indique si l\'utilisateur est administrateur'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Date de création'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Date de mise à jour'
    )
    
    # Relation avec Role (ManyToMany)
    roles = models.ManyToManyField(
        'Role',
        related_name='users',
        blank=True
    )
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    class Meta:
        db_table = 'Users'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['username']),
        ]
    
    def __str__(self):
        return f"{self.username} ({self.email})"
    
    def has_perm(self, perm, obj=None):
        """Vérifier les permissions (simplifié pour l'admin)"""
        return self.is_admin
    
    def has_module_perms(self, app_label):
        """Vérifier les permissions de module"""
        return self.is_admin
    
    @property
    def is_staff(self):
        """Indique si l'utilisateur peut accéder à l'admin Django"""
        return self.is_admin


class Role(models.Model):
    """
    Modèle Role pour gérer les rôles des utilisateurs
    Exemples: 'admin', 'editor', 'viewer', 'uploader'
    """
    uuid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name='UUID'
    )
    name = models.CharField(
        max_length=50,
        unique=True,
        verbose_name='Nom du rôle',
        help_text='Nom unique du rôle (ex: admin, editor, viewer)'
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name='Description',
        help_text='Description du rôle et de ses permissions'
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
        db_table = 'Roles'
        verbose_name = 'Rôle'
        verbose_name_plural = 'Rôles'
        ordering = ['name']
    
    def __str__(self):
        return self.name
