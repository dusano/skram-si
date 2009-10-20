import logging
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.http import require_POST
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core import urlresolvers
from google.appengine.ext import db
from appengine_django import models
from google.appengine.ext.db import djangoforms
import openidgae
from openidgae.decorators import openid_login_required
import SkramSiTwitter
import skram.blog.models

def render(request, response, template, payload):
    person = openidgae.get_current_person(request, response)
    payload['lip'] = person
    payload['user_is_registred'] = (person is not None) and \
        (person.usertype >= openidgae.models.USERTYPE_USER)
    payload['user_is_scrummaster'] = (person is not None) and \
        (person.usertype >= openidgae.models.USERTYPE_SCRUMMASTER)
    payload['user_is_admin'] = (person is not None) and \
        (person.usertype >= openidgae.models.USERTYPE_ADMINISTRATOR)
    return render_to_response(template, 
                              payload, 
                              context_instance=RequestContext(request))

def index(request):
    response = HttpResponse()
    person = openidgae.get_current_person(request, response)
    if (person is not None) and (person.usertype >= openidgae.models.USERTYPE_SCRUMMASTER):
        blog_entries = skram.blog.models.BlogEntry.all()
    else:
        blog_entries = skram.blog.models.BlogEntry.all().filter('is_published =', True)
    payload = dict(blog_entries=blog_entries)
    return render(request, response, 'index.html', payload)

def about_scrum(request):
    return render(request, HttpResponse(), 'about_scrum.html', dict())

# Twitter status update
class TwitterStatus(models.BaseModel):
    twitter_status = db.StringProperty(required=True)

class TwitterStatusUpdateForm(djangoforms.ModelForm):
    class Meta:
        model = TwitterStatus

@openid_login_required(openidgae.models.USERTYPE_SCRUMMASTER)
@require_POST
def twitter_status_update(request):
    status_update_form = TwitterStatusUpdateForm(request.POST)
    if not status_update_form.is_valid():
        return HttpResponseBadRequest('Invalid form: ' + str(status_update_form.errors))
    
    status = status_update_form.cleaned_data['twitter_status'];
    logging.info('twitter.com/skramsi status update: ' + status)
    
    SkramSiTwitter.post_status_update(status)

    return HttpResponseRedirect(urlresolvers.reverse('skram.views.index'))