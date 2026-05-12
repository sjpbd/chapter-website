from django.contrib.admin import AdminSite

class SJPAdminSite(AdminSite):
    site_header = "SJP Chapter 2027"
    site_title = "SJP Chapter 2027 Admin Portal"
    index_title = "Welcome to SJP Chapter 2027 Portal"

sjp_admin_site = SJPAdminSite(name='sjp_admin')
