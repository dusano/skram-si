import logging
from django.http import HttpResponse
from django.views.decorators.http import require_POST
import openidgae
from openidgae import models
from openidgae.decorators import openid_login_required
import skram.views

@openid_login_required(openidgae.models.USERTYPE_ADMINISTRATOR)
def index(request):
    persons = openidgae.models.Person.all();
    usertypes = ({'type':openidgae.models.USERTYPE_USER, 'name':'Uporabnik'},
                 {'type':openidgae.models.USERTYPE_SCRUMMASTER, 'name':'Mojster skrama'},
                 {'type':openidgae.models.USERTYPE_ADMINISTRATOR, 'name':'Administrator'})
    return skram.views.render(request, HttpResponse(), 'users.html', \
                              {'persons': persons, 'usertypes': usertypes})

@openid_login_required(openidgae.models.USERTYPE_ADMINISTRATOR)
@require_POST
def usertype_update(request, openID, userType):
    try:
        persons = models.Person.gql('WHERE openid = :1', openID)
        if persons.count() == 0:
            raise Exception('User with OpenID %s does not exist!' % openID)
        if persons.count() > 1:
            raise Exception('More than one user with OpenID %s!' % openID)
        
        p = persons[0]
        p.usertype = int(userType)
        p.put()
    except Exception, e:
        logging.error('Exception: ' + str(e))
        return HttpResponse(content='Exception: ' + str(e), status=400)
    
    return HttpResponse(content='200 ok', status=200)