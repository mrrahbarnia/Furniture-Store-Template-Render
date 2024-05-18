from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView
)

urlpatterns = [
    path('admin/', admin.site.urls),

    # ========== Store URL's ========== #
    path('', include('store.urls')),
    path('store/api/v1/', include('store.api.v1.urls')),

    # ========== Users URL's ========== #
    path('users/', include('users.urls')),
    path('accounts/api/v1/', include('users.api.v1.urls')),

    # ========== API schema generator ========== #
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path(
        'api/', SpectacularSwaggerView.as_view(url_name='schema'),
        name='swagger-ui'
    ),
]

if settings.DEBUG:
    urlpatterns.append(path('silk/', include('silk.urls', namespace='silk')))
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT
    )
