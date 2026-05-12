from django.db import models
import uuid

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    icon = models.CharField(max_length=50, help_text="Lucide icon name", default="folder")
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)
    show_in_sidebar = models.BooleanField(default=True, help_text="Show this category in the sidebar filters")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['order', 'name']

class ChapterDocument(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    file = models.FileField(upload_to='documents/')
    category = models.ForeignKey(Category, related_name='documents', on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title

class HomeSlider(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.TextField(blank=True)
    image = models.ImageField(upload_to='sliders/')
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    link = models.URLField(blank=True, help_text="Optional link for the slider button")

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title

class SiteStat(models.Model):
    value = models.CharField(max_length=50)
    label = models.CharField(max_length=100)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.value} {self.label}"

class Feature(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.CharField(max_length=50, help_text="Lucide icon name (e.g., BookOpen, Shield)")
    color = models.CharField(max_length=20, default="#0078d4", help_text="Hex color code")
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title
