from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import viewsets

from ..models import Batch, Section
from ..serializers import BatchSerializer


class BatchView(viewsets.ModelViewSet):
    serializer_class = BatchSerializer
    queryset = Batch.objects.all()
