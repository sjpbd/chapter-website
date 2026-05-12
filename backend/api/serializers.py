from rest_framework import serializers
from .models import Category, ChapterDocument, HomeSlider, Feature, SiteStat

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
