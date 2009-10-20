from google.appengine.ext import db
from appengine_django import models
from django.template.defaultfilters import slugify
    
class Poll(models.BaseModel):
    question = db.StringProperty()
    created_on = db.DateTimeProperty(auto_now_add = 1)
    created_by = db.UserProperty()

    def __init__(self, *args, **kw):
        # Add key name based on question
        kw['key_name'] = slugify(kw['question'])
        # Call the constructor of the base class
        db.Model.__init__(self, *args, **kw)

    def __str__(self):
        return '%s' %self.question

    def get_absolute_url(self):
        return '/poll/%s/' % self.key().name()

    def put(self):
        db.Model.put(self)
    
    def delete(self):
        for choice in Choice.all().filter('poll = ', self):
            choice.delete()
        db.Model.delete(self)

class Choice(models.BaseModel):
    poll = db.ReferenceProperty(Poll)
    choice = db.StringProperty()
    votes = db.IntegerProperty(default = 0)