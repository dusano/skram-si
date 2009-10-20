from google.appengine.ext import db
from django.template.defaultfilters import slugify
from django.db import models
from openidgae.models import Person

class BlogEntry(db.Model):
    """Each blog entry.
    Title: Post title.
    Slug: Post slug. These two if not given are inferred directly from entry text.
    text = The main data for the post.
    summary = The summary for the text. probably can can be derived from text, bit we dont want do do that each time main page is displayed.
    created_on = The date this entry was created. Defaults to now.
    Created by: The user who wrote this.
    is_published: Is this page published. If yes then we would display this on site, otherwise no. Default to true.
    comments_allowed: Are comments allowed on this post? Default to True"""
    title = db.StringProperty(verbose_name='Naslov', required=True)
    text = db.TextProperty(verbose_name='Besedilo')
    created_on = db.DateTimeProperty(verbose_name='Ustvarjeno', auto_now_add = 1)
    created_by = db.ReferenceProperty(verbose_name='Ustvaril', reference_class=Person)
    is_published = db.BooleanProperty(verbose_name='Objavljeno', default = False)
    comments_allowed = db.BooleanProperty(verbose_name='Dovoljeni komentarji', default = True)

    def __init__(self, *args, **kw):
        # Add key name based on question
        kw['key_name'] = slugify(kw['title'])
        # Call the constructor of the base class
        db.Model.__init__(self, *args, **kw)
        
    def __unicode__(self):
        return u'%s' % self.title

    def __str__(self):
        return self.__unicode__()

    @models.permalink
    def get_absolute_url(self):
        return ('skram.blog.views.blog_entry', [self.key().name()])
    
    def delete(self):
        for comment in Comment.all().filter('entry = ', self):
            comment.delete()
        db.Model.delete(self)

class Comment(db.Model):
    """Comments for each blog.
    text: The comment text.
    blog_entry: the Post/Page this comment is created for.
    created_on: The date this comment was written on.
    created_by: THe user who wrote this comment.
    is_spam: Is comment marked as spam? We do not display the comment in those cases."""
    text = db.TextProperty()
    blog_entry = db.ReferenceProperty(BlogEntry, collection_name='comments')
    created_on = db.DateTimeProperty(auto_now_add = True)
    created_by = db.ReferenceProperty(reference_class=Person, required=True, collection_name='comments')
    is_spam = db.BooleanProperty(default = False)

    @models.permalink
    def get_absolute_url(self):
        return ('skram.blog.views.delete_blog_comment', [self.blog_entry.key().name(), self.key().id()])
    
    def __str__(self):
        return self.text
