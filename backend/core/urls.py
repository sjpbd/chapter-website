from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Customize Django Admin Header
admin.site.site_header = "SJP Chapter 2027"
admin.site.site_title = "SJP Chapter 2027 Admin Portal"
admin.site.index_title = "Welcome to SJP Chapter 2027 Portal"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
