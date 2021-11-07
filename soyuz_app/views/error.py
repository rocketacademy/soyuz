# HttpResponseBadRequest
# HttpResponseNotFound
# HttpResponseForbidden
# HttpResponseNotAllowed
# HttpResponseGone
from django.http import HttpResponseNotFound, HttpResponseServerError
from sentry_sdk import capture_message


def error_404(*args, **kwargs):
    capture_message("Page not found!", level="error")

    return HttpResponseNotFound("Sorry!!! Not found, my friend.")


def error_500(*args, **kwargs):
    capture_message("Fail whale!", level="error")

    return HttpResponseServerError("Sorry error!")
