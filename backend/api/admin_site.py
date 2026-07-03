from django.contrib.admin import AdminSite

class SJPAdminSite(AdminSite):
    site_header = "SJP Chapter 2027"
    site_title = "SJP Chapter 2027 Admin Portal"
    index_title = "Welcome to SJP Chapter 2027 Portal"

    def each_context(self, request):
        context = super().each_context(request)
        from .models import SiteConfiguration
        try:
            config = SiteConfiguration.objects.first()
            if config:
                context['site_logo'] = config.logo.url if config.logo else None
                context['site_name'] = config.site_name
            else:
                context['site_logo'] = None
                context['site_name'] = "SJP Chapter Hub"
        except Exception:
            context['site_logo'] = None
            context['site_name'] = "SJP Chapter Hub"
        return context

sjp_admin_site = SJPAdminSite(name='sjp_admin')
