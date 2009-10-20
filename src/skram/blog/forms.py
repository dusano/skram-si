from google.appengine.ext.db import djangoforms
import models

class BlogEntryForm(djangoforms.ModelForm):
    class Meta:
        model = models.BlogEntry
        exclude = ['created_by']
