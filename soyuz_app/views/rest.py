from rest_framework import viewsets

from ..models import Batch
from ..serializers import BatchSerializer


class BatchView(viewsets.ModelViewSet):
    serializer_class = BatchSerializer
    queryset = Batch.objects.all()
