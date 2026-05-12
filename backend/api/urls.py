from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, ChapterDocumentViewSet, HomeSliderViewSet, FeatureViewSet, SiteStatViewSet

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'documents', ChapterDocumentViewSet)
router.register(r'sliders', HomeSliderViewSet)
router.register(r'features', FeatureViewSet)
router.register(r'stats', SiteStatViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
