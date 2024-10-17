from django.contrib import admin
from django.urls import path, include

from .routers import router

from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/user/', include("apps.user.urls")),
    path('api/', include(router.urls)),

    # SWAGGER
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]
