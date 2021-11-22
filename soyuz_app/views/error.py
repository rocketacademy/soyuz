# HttpResponseBadRequest
# HttpResponseNotFound
# HttpResponseForbidden
# HttpResponseNotAllowed
# HttpResponseGone
from django.shortcuts import render
from sentry_sdk import capture_message


def custom_error_404(request, exception):
    capture_message("page not found", level="error")
    return render(request, '404.html')


def custom_error_500(request):
    capture_message("Fail whale!", level="error")
    return render(request, '500.html')
