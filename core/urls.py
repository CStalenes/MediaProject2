from django.contrib import admin
from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
#from home.swagger import schema_view

urlpatterns = [
    path('admin/', admin.site.urls),
    #path('swagger/', schema_view.with_ui('swagger',
                                         #cache_timeout=0), name='schema-swagger-ui'),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # REDOC + Swagger UI, vous avez le choix ! 

    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc-ui'),
    path('api/healthcheck/', HealthCheckView.as_view(), name='healthcheck'),
    path('api/version/', VersionView.as_view(), name='version')
]

