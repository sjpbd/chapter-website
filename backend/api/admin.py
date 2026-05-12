from django.contrib import admin
from .models import Category, ChapterDocument, HomeSlider, Feature, SiteStat

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'order', 'show_in_sidebar']
    list_editable = ['order', 'show_in_sidebar']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(ChapterDocument)
class ChapterDocumentAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'uploaded_at']
    list_filter = ['category']
    search_fields = ['title', 'description']

@admin.register(HomeSlider)
class HomeSliderAdmin(admin.ModelAdmin):
    list_display = ['title', 'order', 'is_active']
    list_editable = ['order', 'is_active']

@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    list_display = ['title', 'icon', 'order', 'is_active']
    list_editable = ['order', 'is_active']

@admin.register(SiteStat)
class SiteStatAdmin(admin.ModelAdmin):
    list_display = ['label', 'value', 'order', 'is_active']
    list_editable = ['order', 'is_active']
