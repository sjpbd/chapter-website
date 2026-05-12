from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Category, ChapterDocument, HomeSlider, Feature, SiteStat
from .serializers import CategorySerializer, ChapterDocumentSerializer, HomeSliderSerializer, FeatureSerializer, SiteStatSerializer

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all().order_by('order', 'name')
    serializer_class = CategorySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['show_in_sidebar']

class ChapterDocumentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ChapterDocument.objects.all().order_by('-uploaded_at')
    serializer_class = ChapterDocumentSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category']
    search_fields = ['title', 'description']
    ordering_fields = ['uploaded_at', 'title']

class HomeSliderViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = HomeSlider.objects.filter(is_active=True)
    serializer_class = HomeSliderSerializer

class FeatureViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Feature.objects.filter(is_active=True)
    serializer_class = FeatureSerializer

class SiteStatViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SiteStat.objects.filter(is_active=True)
    serializer_class = SiteStatSerializer
