from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .viewsets import EventViewSet, ReviewViewSet

router = DefaultRouter()
router.register(r'events', EventViewSet, basename='api-events')
router.register(r'reviews', ReviewViewSet, basename='api-reviews')

urlpatterns = [
    path('', include(router.urls)),
]
