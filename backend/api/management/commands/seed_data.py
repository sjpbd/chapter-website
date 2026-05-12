"""
Management command to seed sample data for SJP Chapter Hub.
Run: python manage.py seed_data
"""
from django.core.management.base import BaseCommand
from api.models import Category, ChapterDocument, HomeSlider
from django.core.files.base import ContentFile
import os


CATEGORIES = [
    {"name": "Chapter Acts",        "slug": "chapter-acts",        "icon": "file-text",    "description": "Official acts passed at provincial chapters."},
    {"name": "Constitutions",       "slug": "constitutions",        "icon": "book-open",    "description": "Provincial and congregational constitutions."},
    {"name": "Directory",           "slug": "directory",            "icon": "users",        "description": "Provincial directory of members and communities."},
    {"name": "Meeting Minutes",     "slug": "meeting-minutes",      "icon": "clipboard",    "description": "Minutes from provincial council meetings."},
    {"name": "Circulars",           "slug": "circulars",            "icon": "mail",         "description": "Provincial superior circulars and letters."},
    {"name": "Formation Documents", "slug": "formation-documents",  "icon": "graduation-cap","description": "Documents related to initial and ongoing formation."},
]

SLIDERS = [
    {
        "title":    "Welcome to SJP Chapter Hub",
        "subtitle": "Your trusted digital repository for St. Joseph Province official chapter materials and records.",
        "order":    1,
    },
    {
        "title":    "Preserving Our History",
        "subtitle": "Access decades of provincial wisdom, legislative records, and community milestones.",
        "order":    2,
    },
    {
        "title":    "Download Official Documents",
        "subtitle": "PDFs, DOC files and more — all organized, searchable, and securely available.",
        "order":    3,
    },
]


class Command(BaseCommand):
    help = "Seed the database with sample categories and slider data"

    def handle(self, *args, **options):
        # Categories
        for data in CATEGORIES:
            cat, created = Category.objects.get_or_create(
                slug=data["slug"],
                defaults={"name": data["name"], "icon": data["icon"], "description": data["description"]}
            )
            status = "created" if created else "already exists"
            self.stdout.write(f"  Category '{cat.name}' {status}.")

        # Sliders (need a placeholder image)
        from django.core.files.base import ContentFile
        # 1x1 white pixel PNG
        PIXEL = (
            b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01'
            b'\x08\x02\x00\x00\x00\x90wS\xde\x00\x00\x00\x0cIDATx\x9cc\xf8\x0f\x00'
            b'\x00\x01\x01\x00\x05\x18\xd8n\x00\x00\x00\x00IEND\xaeB`\x82'
        )
        for s in SLIDERS:
            obj, created = HomeSlider.objects.get_or_create(
                order=s["order"],
                defaults={"title": s["title"], "subtitle": s["subtitle"], "is_active": True}
            )
            if created:
                obj.image.save(f"slider_{s['order']}.png", ContentFile(PIXEL), save=True)
                self.stdout.write(f"  Slider '{obj.title}' created.")
            else:
                self.stdout.write(f"  Slider order={s['order']} already exists.")

        self.stdout.write(self.style.SUCCESS("\n✓ Seed data complete. Add real documents via /admin/"))
