from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .models import Test
from .serializers import TestSerializer
from users.permissions import IsTutor


class TestViewSet(ModelViewSet):
    queryset = Test.objects.all()
    serializer_class = TestSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            # Only Tutors can modify tests
            permission_classes = [IsAuthenticated, IsTutor]
        else:
            # Both Students and Tutors can view tests
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
