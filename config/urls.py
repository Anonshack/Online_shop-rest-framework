from django.contrib import admin
from django.urls import path, include
from django.urls import re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
   openapi.Info(
      title="Online_shop API",
      default_version='v1',
      description="information",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="princeasia013@gmail.com"),
      license=openapi.License(name="Anonymouse"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-accounts/', include('users.urls')),
    path('shop-temp/', include('temp.urls')),
    path('api-password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),

#   For API documentation
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
