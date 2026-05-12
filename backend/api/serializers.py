from rest_framework import serializers
from .models import Category, ChapterDocument, HomeSlider, Feature, SiteStat, ChapterPrayer, ScheduleDay, ScheduleEvent

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ChapterDocumentSerializer(serializers.ModelSerializer):
    category_name = serializers.ReadOnlyField(source='category.name')
    
    class Meta:
        model = ChapterDocument
        fields = ['id', 'title', 'description', 'file', 'category', 'category_name', 'uploaded_at', 'updated_at']

class HomeSliderSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomeSlider
        fields = '__all__'

class FeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feature
        fields = '__all__'

class SiteStatSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteStat
        fields = '__all__'

class ChapterPrayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChapterPrayer
        fields = ['id', 'title', 'subtitle', 'body', 'prayer_intention', 'author_attribution', 'updated_at']

class ScheduleEventSerializer(serializers.ModelSerializer):
    category_display = serializers.CharField(source='get_category_display', read_only=True)
    time_start_fmt = serializers.SerializerMethodField()
    time_end_fmt   = serializers.SerializerMethodField()

    class Meta:
        model  = ScheduleEvent
        fields = [
            'id', 'time_start', 'time_end', 'time_start_fmt', 'time_end_fmt',
            'title', 'description', 'location', 'speaker',
            'category', 'category_display', 'is_highlighted', 'order',
        ]

    def _fmt(self, t):
        if not t:
            return None
        hour = t.hour % 12 or 12
        suffix = 'AM' if t.hour < 12 else 'PM'
        return f"{hour}:{t.minute:02d} {suffix}"

    def get_time_start_fmt(self, obj): return self._fmt(obj.time_start)
    def get_time_end_fmt(self, obj):   return self._fmt(obj.time_end)

class ScheduleDaySerializer(serializers.ModelSerializer):
    events = ScheduleEventSerializer(many=True, read_only=True)
    date_fmt = serializers.SerializerMethodField()
    weekday  = serializers.SerializerMethodField()

    class Meta:
        model  = ScheduleDay
        fields = ['id', 'date', 'date_fmt', 'weekday', 'day_label', 'theme', 'order', 'events']

    def get_date_fmt(self, obj):
        return obj.date.strftime('%d %B %Y')

    def get_weekday(self, obj):
        return obj.date.strftime('%A')

