from django.http import HttpResponse
import skram.views

def index(request):
    return skram.views.render(request, HttpResponse(), 'scrummaster.html', dict())