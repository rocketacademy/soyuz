# HttpResponseBadRequest
# HttpResponseNotFound
# HttpResponseForbidden
# HttpResponseNotAllowed
# HttpResponseGone
from django.shortcuts import render
from sentry_sdk import capture_message


def error_404(request, exception):
    capture_message("page not found", level="error")
    message = 'Page not found, my friend!'
    return render(request, 'error-page.html', {'message': message})


def error_500(request):
    capture_message("Fail whale!", level="error")
    message = 'Sorry! Error'
    return render(request, 'error-page.html', {'message': message})
