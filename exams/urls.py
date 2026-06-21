from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TestViewSet, SubmissionViewSet # Add your new viewset here!

router = DefaultRouter()
router.register(r'tests', TestViewSet)

# The new secure endpoint!
router.register(r'my-results', SubmissionViewSet, basename='my-results')

urlpatterns = [
    path('', include(router.urls)),
]