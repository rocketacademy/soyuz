from django.shortcuts import render

from django.http import HttpResponse
from ..models import Batch,Section

def index(request):
    batches = Batch.objects.all()

    context = {
        "title":"index",
        "batches": batches,
    }

    return render(request, "index.html", context)
