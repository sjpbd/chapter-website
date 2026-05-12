from django.db import models
import uuid
from django.core.exceptions import ValidationError

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


class ChapterPrayer(models.Model):
    """Singleton model — only one row should exist. Admins edit the prayer here."""
    title = models.CharField(
        max_length=200,
        default="Prayer for the St. Joseph Province Chapter 2027",
        help_text="The heading displayed on the prayer card"
    )
    subtitle = models.CharField(
        max_length=300,
        blank=True,
        default="A Prayer of Hope, Mission & Renewal",
        help_text="Displayed below the title as a decorative tagline"
    )
    # Body is stored as plain text; line breaks are honoured in the template
    body = models.TextField(
        help_text="Full prayer text. Use blank lines to separate stanzas/paragraphs.",
        default=(
            "Heavenly Father,\n\n"
            "We come before You with hearts full of gratitude and hope,\n"
            "as we prepare to gather in Chapter for the St. Joseph Province in 2027.\n\n"
            "Grant us, O Lord, the wisdom of St. Joseph —\n"
            "that quiet, steadfast trust that discerns Your will in every season,\n"
            "and the courage to act upon it with humble obedience.\n\n"
            "Breathe into our assembly the fire of Your Holy Spirit,\n"
            "that our deliberations may not be mere human striving,\n"
            "but a listening — attentive, patient, and docile —\n"
            "to where You are calling our Province in this hour.\n\n"
            "May our Chapter be a moment of grace:\n"
            "a time to renew our Salesian consecration,\n"
            "to deepen our fraternal bonds,\n"
            "and to recommit ourselves to the young\n"
            "who walk in darkness and await the light of Don Bosco's charism.\n\n"
            "Bless each capitulant and all who serve in preparation.\n"
            "Guard our Province in unity, truth, and joy.\n"
            "Let our decisions bear fruit for generations to come,\n"
            "to the glory of Your name and the salvation of souls.\n\n"
            "We ask this through Christ our Lord,\n"
            "in the company of Mary Help of Christians\n"
            "and our Father and Founder, St. John Bosco.\n\n"
            "Amen."
        )
    )
    prayer_intention = models.CharField(
        max_length=400,
        blank=True,
        default="For wisdom, unity, and the renewal of our Salesian mission.",
        help_text="Short intention line displayed at the bottom of the card"
    )
    author_attribution = models.CharField(
        max_length=200,
        blank=True,
        default="St. Joseph Province — Bangladesh",
        help_text="Attribution line at the foot of the prayer"
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Show this prayer on the website"
    )
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Chapter Prayer"
        verbose_name_plural = "Chapter Prayer"

    def clean(self):
        # Enforce singleton — only one active record allowed
        if self.is_active:
            qs = ChapterPrayer.objects.filter(is_active=True)
            if self.pk:
                qs = qs.exclude(pk=self.pk)
            if qs.exists():
                raise ValidationError("Only one active Chapter Prayer is allowed at a time.")

    def __str__(self):
        return self.title


class ScheduleDay(models.Model):
    """One chapter day — groups all events for that date."""
    date = models.DateField(help_text="Calendar date for this chapter day")
    day_label = models.CharField(
        max_length=100,
        help_text="Short label, e.g. 'Day 1 — Opening', 'Day 2 — Deliberations'",
    )
    theme = models.CharField(
        max_length=200, blank=True,
        help_text="Optional theme or subtitle for the day"
    )
    order = models.PositiveIntegerField(default=0, help_text="Display order")
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order', 'date']
        verbose_name = "Schedule Day"
        verbose_name_plural = "Schedule Days"

    def __str__(self):
        return f"{self.date.strftime('%d %b %Y')} — {self.day_label}"


class ScheduleEvent(models.Model):
    """A single programme item within a chapter day."""

    CATEGORY_CHOICES = [
        ('liturgy',  '🙏 Liturgy / Prayer'),
        ('session',  '📋 Session / Working Group'),
        ('keynote',  '🎤 Keynote / Talk'),
        ('meal',     '🍽️ Meal / Refreshment'),
        ('break',    '☕ Break'),
        ('social',   '🤝 Social / Recreation'),
        ('travel',   '🚌 Travel / Transfer'),
        ('other',    '📌 Other'),
    ]

    day = models.ForeignKey(
        ScheduleDay, related_name='events',
        on_delete=models.CASCADE
    )
    time_start = models.TimeField(help_text="Start time (24-hour or AM/PM)")
    time_end = models.TimeField(null=True, blank=True, help_text="End time (optional)")
    title = models.CharField(max_length=255, help_text="Programme title")
    description = models.TextField(blank=True, help_text="Details, agenda notes, etc.")
    location = models.CharField(max_length=200, blank=True, help_text="Room, venue, or place")
    speaker = models.CharField(max_length=200, blank=True, help_text="Speaker / presider name(s)")
    category = models.CharField(
        max_length=20, choices=CATEGORY_CHOICES, default='session'
    )
    is_highlighted = models.BooleanField(
        default=False, help_text="Pin this event as important (shown with extra emphasis)"
    )
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order', 'time_start']
        verbose_name = "Schedule Event"
        verbose_name_plural = "Schedule Events"

    def __str__(self):
        return f"{self.time_start.strftime('%H:%M')} — {self.title}"
