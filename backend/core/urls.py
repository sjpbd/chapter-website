from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from api.admin_site import sjp_admin_site

urlpatterns = [
    path('admin/', sjp_admin_site.urls),
    path('api/', include('api.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
