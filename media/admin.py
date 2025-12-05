from django.contrib import admin
from media.models import Media, MediaJob, HttpUrl


@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    """Configuration de l'admin pour le modèle Media"""
    list_display = [
        'uuid', 
        'original_filename', 
        'file_type', 
        'uploader', 
        'file_size', 
        'created_at'
    ]
    list_filter = ['file_type', 'created_at', 'uploader']
    search_fields = [
        'original_filename', 
        'imagekit_file_id', 
        'imagekit_url', 
        'uploader__username',
        'uploader__email'
    ]
    readonly_fields = [
        'uuid', 
        'created_at', 
        'updated_at',
        'imagekit_file_id',
        'imagekit_url',
        'imagekit_thumbnail_url'
    ]
    ordering = ['-created_at']
    
    fieldsets = (
        ('Informations de base', {
            'fields': ('uuid', 'uploader', 'original_filename', 'file_type')
        }),
        ('Métadonnées du fichier', {
            'fields': ('file_size', 'mime_type', 'width', 'height', 'duration_s')
        }),
        ('ImageKit', {
            'fields': ('imagekit_file_id', 'imagekit_url', 'imagekit_thumbnail_url')
        }),
        ('Dates', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(MediaJob)
class MediaJobAdmin(admin.ModelAdmin):
    """Configuration de l'admin pour le modèle MediaJob"""
    list_display = [
        'uuid',
        'media',
        'job_type',
        'status',
        'started_at',
        'completed_at',
        'created_at'
    ]
    list_filter = ['status', 'job_type', 'created_at']
    search_fields = [
        'media__original_filename',
        'media__imagekit_file_id',
        'error_message'
    ]
    readonly_fields = [
        'uuid',
        'created_at',
        'updated_at',
        'started_at',
        'completed_at'
    ]
    ordering = ['-created_at']
    
    fieldsets = (
        ('Informations de base', {
            'fields': ('uuid', 'media', 'job_type', 'status')
        }),
        ('Traitement', {
            'fields': ('started_at', 'completed_at', 'error_message', 'result_data')
        }),
        ('Dates', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(HttpUrl)
class HttpUrlAdmin(admin.ModelAdmin):
    """Configuration de l'admin pour le modèle HttpUrl"""
    list_display = [
        'url',
        'url_type',
        'status',
        'status_code',
        'media',
        'created_by',
        'expires_at',
        'last_checked_at',
        'created_at'
    ]
    list_filter = ['url_type', 'status', 'http_method', 'created_at', 'expires_at']
    search_fields = [
        'url',
        'title',
        'description',
        'media__original_filename',
        'created_by__username',
        'created_by__email'
    ]
    readonly_fields = [
        'uuid',
        'created_at',
        'updated_at',
        'last_checked_at',
        'status_code'
    ]
    ordering = ['-created_at']
    
    fieldsets = (
        ('URL', {
            'fields': ('uuid', 'url', 'url_type', 'status', 'title', 'description')
        }),
        ('Relations', {
            'fields': ('media', 'created_by')
        }),
        ('Informations HTTP', {
            'fields': ('http_method', 'status_code', 'last_checked_at', 'expires_at')
        }),
        ('Métadonnées', {
            'fields': ('tags', 'metadata'),
            'classes': ('collapse',)
        }),
        ('Dates', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    
    def get_queryset(self, request):
        """Optimiser les requêtes avec select_related"""
        qs = super().get_queryset(request)
        return qs.select_related('media', 'created_by')
