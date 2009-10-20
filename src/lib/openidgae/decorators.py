from functools import wraps
from django.http import HttpResponse
import openidgae

def openid_login_required(min_authorization_level):
    """
    Decorator for views that checks that the user is logged in using OpenID
    """
    def decorator(func):
        def inner(request, *args, **kwargs):
            lip = openidgae.get_current_person(request, HttpResponse())
            if (lip is None) or (lip.usertype < min_authorization_level):
                return HttpResponse(content='401 unauthorized', status=401)
            return func(request, *args, **kwargs)
        return wraps(func)(inner)
    return decorator