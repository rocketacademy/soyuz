from django.http import HttpResponse
from django.shortcuts import render

from rest_framework import viewsets
from ..serializers import BatchSerializer
from ..models import Batch,Section

class BatchView(viewsets.ModelViewSet):
    serializer_class = BatchSerializer
    queryset = Batch.objects.all()
