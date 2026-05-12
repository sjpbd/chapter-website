from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.utils.html import format_html
from .models import Category, ChapterDocument, HomeSlider, Feature, SiteStat, ChapterPrayer, ScheduleDay, ScheduleEvent, SiteConfiguration
from .admin_site import sjp_admin_site

# Registering built-in Auth models to custom site
sjp_admin_site.register(User)
sjp_admin_site.register(Group)

@admin.register(Category, site=sjp_admin_site)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'order', 'show_in_sidebar']
    list_editable = ['order', 'show_in_sidebar']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(ChapterDocument, site=sjp_admin_site)
class ChapterDocumentAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'uploaded_at']
    list_filter = ['category']
    search_fields = ['title', 'description']

@admin.register(HomeSlider, site=sjp_admin_site)
class HomeSliderAdmin(admin.ModelAdmin):
    list_display = ['title', 'order', 'is_active']
    list_editable = ['order', 'is_active']

@admin.register(Feature, site=sjp_admin_site)
class FeatureAdmin(admin.ModelAdmin):
    list_display = ['title', 'icon', 'order', 'is_active']
    list_editable = ['order', 'is_active']

@admin.register(SiteStat, site=sjp_admin_site)
class SiteStatAdmin(admin.ModelAdmin):
    list_display = ['label', 'value', 'order', 'is_active']
    list_editable = ['order', 'is_active']


@admin.register(ChapterPrayer, site=sjp_admin_site)
class ChapterPrayerAdmin(admin.ModelAdmin):
    list_display = ['title', 'author_attribution', 'is_active', 'updated_at']
    list_editable = ['is_active']
    fieldsets = (
        ('📖 Prayer Identity', {
            'fields': ('title', 'subtitle', 'is_active'),
            'description': 'The heading and tagline displayed prominently on the Prayer Card page.',
        }),
        ('✍️ Prayer Body', {
            'fields': ('body',),
            'description': (
                'Enter the full prayer text. Use blank lines to separate stanzas or paragraphs. '
                'Line breaks are preserved on the website.'
            ),
        }),
        ('🕊️ Footer Details', {
            'fields': ('prayer_intention', 'author_attribution'),
            'description': 'Short intention and attribution shown at the foot of the prayer card.',
        }),
    )

    def has_add_permission(self, request):
        return not ChapterPrayer.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser


class ScheduleEventInline(admin.TabularInline):
    model = ScheduleEvent
    extra = 3
    fields = ['order', 'time_start', 'time_end', 'title', 'category', 'location', 'speaker', 'description', 'is_highlighted', 'is_active']
    ordering = ['order', 'time_start']


@admin.register(ScheduleDay, site=sjp_admin_site)
class ScheduleDayAdmin(admin.ModelAdmin):
    list_display  = ['date', 'day_label', 'theme', 'event_count', 'order', 'is_active']
    list_editable = ['order', 'is_active']
    list_filter   = ['is_active']
    ordering      = ['order', 'date']
    inlines       = [ScheduleEventInline]
    fieldsets = (
        ('📅 Day Details', {
            'fields': ('date', 'day_label', 'theme', 'order', 'is_active'),
            'description': (
                'Set the calendar date and a short label (e.g. "Day 1 — Arrival & Opening"). '
                'Then add all programme events in the table below.'
            ),
        }),
    )

    @admin.display(description='Events')
    def event_count(self, obj):
        count = obj.events.filter(is_active=True).count()
        return format_html('<b>{}</b> events', count)



@admin.register(SiteConfiguration, site=sjp_admin_site)
class SiteConfigurationAdmin(admin.ModelAdmin):
    list_display = ['site_name']
    
    def has_add_permission(self, request):
        return not SiteConfiguration.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False # Prevent deletion of site config
