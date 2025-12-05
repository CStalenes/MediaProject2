from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from core.models import User, Role


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Configuration de l'admin pour le modèle User"""
    list_display = ['uuid', 'username', 'email', 'is_active', 'is_admin', 'created_at']
    list_filter = ['is_active', 'is_admin', 'created_at']
    search_fields = ['username', 'email', 'uuid']
    readonly_fields = ['uuid', 'created_at', 'updated_at']
    ordering = ['-created_at']
    
    fieldsets = (
        (None, {'fields': ('uuid', 'email', 'username', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_admin', 'roles')}),
        ('Dates', {'fields': ('created_at', 'updated_at')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'is_active', 'is_admin'),
        }),
    )


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    """Configuration de l'admin pour le modèle Role"""
    list_display = ['uuid', 'name', 'description', 'created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['uuid', 'created_at', 'updated_at']
    ordering = ['name']
