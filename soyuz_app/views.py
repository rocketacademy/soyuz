from django.shortcuts import render

from django.http import HttpResponse

from django.shortcuts import render
from rest_framework import viewsets
from .serializers import BatchSerializer
from .models import Batch,Section

# ============================================
# ============================================
# ============================================
#               REST Views
# ============================================
# ============================================
# ============================================
# ============================================

class BatchView(viewsets.ModelViewSet):
    serializer_class = BatchSerializer
    queryset = Batch.objects.all()

# ============================================
# ============================================
# ============================================
#               Views
# ============================================
# ============================================
# ============================================
# ============================================
def index(request):
    # send back a text response
    return HttpResponse("Hello, world. You're at the index.")
