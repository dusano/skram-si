from django.conf import settings
import models

COOKIE_NAME = 'skram_si_sess'
if hasattr(settings, 'SKRAM_SI_COOKIE_NAME'):
    COOKIE_NAME = settings.SKRAM_SI_COOKIE_NAME


def get_session_id_from_cookie(request):
    if request.COOKIES.has_key(COOKIE_NAME):
        return request.COOKIES[COOKIE_NAME]

    return None


def write_session_id_cookie(response, session_id):
    import datetime
    expires = datetime.datetime.now() + datetime.timedelta(weeks=2)
    expires_rfc822 = expires.strftime('%a, %d %b %Y %H:%M:%S +0000')
    response.set_cookie(COOKIE_NAME, session_id, expires=expires_rfc822)


def get_session(request, response, create=True):
    if hasattr(request, 'skram_si_session'):
        return request.skram_si_session

    # get existing session

    session_id = get_session_id_from_cookie(request)
    if session_id:
        session = models.Session.get_by_key_name(session_id)
        if session is not None:
            request.skram_si_session = session
            return request.skram_si_session

    if create:
        request.skram_si_session = models.Session()
        request.skram_si_session.put()
        write_session_id_cookie(response,
                                request.skram_si_session.key().name())
        return request.skram_si_session

    return None

def get_current_person(request, response):
    if hasattr(request, 'skram_si_logged_in_person'):
        return request.skram_si_logged_in_person

    s = get_session(request, response, create=False)
    if not s:
        return None

    # Workaround for Google App Engine Bug 426

    from google.appengine.api import datastore_errors
    try:
        request.skram_si_logged_in_person = s.person
    except datastore_errors.Error, e:
        if e.args[0] == 'ReferenceProperty failed to be resolved':
            return None
        else:
            raise

    return request.skram_si_logged_in_person


