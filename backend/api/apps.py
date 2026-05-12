from django.apps import AppConfig


class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'

    def ready(self):
        from django.contrib import admin
        admin.site.site_header = "SJP Chapter 2027"
        admin.site.site_title = "SJP Chapter 2027 Admin Portal"
        admin.site.index_title = "Welcome to SJP Chapter 2027 Portal"
