from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="ZC Bus API",
        default_version='v1',
        description="This is the schema for ZC Bus service (A gift from backend to frontend)",
    ),
    public=True,
    permission_classes=[permissions.AllowAny,],
)

urlpatterns = [
    # Main URLs
    path('admin/', admin.site.urls),
    path('user/', include('apps.users.urls')),
    path('bus/', include('apps.bus.urls')),
    path('subscription/', include('apps.subscription.urls')),
    path('semester/', include('apps.semester.urls')),
    # Swagger URLs
    path('api/docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
