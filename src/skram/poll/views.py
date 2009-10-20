from django.http import HttpResponse, HttpResponseRedirect
from skram.poll import models
import bforms
from django.shortcuts import render_to_response
from django.core.exceptions import ObjectDoesNotExist
import openidgae
import django.core.urlresolvers

def render(request, response, template, payload):
    payload['recents'] = models.Poll.all().order('-created_on').fetch(20)
    payload['lip'] = openidgae.get_current_person(request, response)
    return render_to_response(template, payload)

def create(request):
    if request.method == 'GET':
        pollform = bforms.PollForm()
        choiceforms = []
        for i in range(4):
            choiceforms.append(bforms.ChoiceForm(prefix = 'f%s'%i))
    if request.method == 'POST':
        pollform = bforms.PollForm(request.POST)
        if pollform.is_valid():
#            pollform.instance = models.Poll.get_or_insert(pollform.clean_data['question'])
            poll = pollform.save()
            choiceforms = []
            for i in range(4):
                choiceforms.append(bforms.ChoiceForm(poll=poll, prefix = 'f%s'%i, data=request.POST))
            for form in choiceforms:
                if form.is_valid():
                    form.save()
            return HttpResponseRedirect(poll.get_absolute_url())
    payload = dict(pollform=pollform, choiceforms=choiceforms)
    return render(request, HttpResponse(), 'create.html', payload)

def delete(request, poll_key):
    poll = models.Poll.get_by_key_name(poll_key)
    if poll is None:
        raise ObjectDoesNotExist('Poll does not exist!')
    poll.delete()
    return HttpResponseRedirect('/')

def poll_detail(request, poll_key):
    poll = models.Poll.get_by_key_name(poll_key)
    choices = models.Choice.all().filter('poll = ', poll)
    if request.method == 'POST':
        choice_key = request.POST['value']
        choice = models.Choice.get(choice_key)
        choice.votes += 1
        choice.put()
        return HttpResponseRedirect('./results/')
    payload = dict(poll = poll, choices = choices)
    return render(request, HttpResponse(), 'poll_details.html', payload)

def poll_results(request, poll_key):
    poll = models.Poll.get_by_key_name(poll_key)
    choices = models.Choice.all().filter('poll = ', poll)
    payload = dict(poll = poll, choices = choices)
    return render(request, HttpResponse(), 'poll_results.html', payload)

def log_me_in(request):
    return HttpResponse('<a href="%s">Login</a>' %
        openidgae.create_login_url(
            django.core.urlresolvers.reverse('openidgae.views.LoginPage')))
