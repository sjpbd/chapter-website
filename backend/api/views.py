from rest_framework import viewsets, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from .models import Category, ChapterDocument, HomeSlider, Feature, SiteStat, ChapterPrayer, ScheduleDay
from .serializers import (
    CategorySerializer, ChapterDocumentSerializer, HomeSliderSerializer,
    FeatureSerializer, SiteStatSerializer, ChapterPrayerSerializer, ScheduleDaySerializer
)

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

class ChapterPrayerView(APIView):
    """Returns the single active Chapter Prayer."""
    def get(self, request):
        prayer = ChapterPrayer.objects.filter(is_active=True).first()
        if not prayer:
            return Response({'detail': 'No active prayer found.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ChapterPrayerSerializer(prayer, context={'request': request})
        return Response(serializer.data)

class ScheduleViewSet(viewsets.ReadOnlyModelViewSet):
    """Returns all active schedule days with their nested events."""
    queryset = (
        ScheduleDay.objects
        .filter(is_active=True)
        .prefetch_related('events')
        .order_by('order', 'date')
    )
    serializer_class = ScheduleDaySerializer

