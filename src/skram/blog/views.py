import logging
from django.http import HttpResponse, HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.core import urlresolvers
from django.views.decorators.http import require_http_methods, require_GET, require_POST
import openidgae
from openidgae.decorators import openid_login_required
import models
import forms
import skram.views

@openid_login_required(openidgae.models.USERTYPE_SCRUMMASTER)
@require_POST
def create_or_update(request, blog_entry=None):
    if request.POST:
        # The POST request includes form data - validate it
        blog_entry_form = forms.BlogEntryForm(request.POST, instance=blog_entry)
        if blog_entry_form.is_valid():
            if blog_entry is None:
                blog_entry = blog_entry_form.save(commit=False)
                blog_entry.created_by = openidgae.get_current_person(request, HttpResponse())
                blog_entry.put()
            else:
                blog_entry = blog_entry_form.save()
            return HttpResponseRedirect(blog_entry.get_absolute_url())
        else:
            response_status = 400;
    else:
        # The POST request does not include form data
        blog_entry_form = forms.BlogEntryForm(instance=blog_entry)
        response_status = 200;
        
    payload = dict(blog_entry_form=blog_entry_form, blog_entry=blog_entry)
    response = skram.views.render(request, HttpResponse(), 'edit_blog_entry.html', payload)
    response.status_code = response_status;
    return response

@require_GET
def read(request, blog_entry):
    payload = dict(blog_entry=blog_entry)
    return skram.views.render(request, HttpResponse(), 'blog_entry.html', payload)

@openid_login_required(openidgae.models.USERTYPE_SCRUMMASTER)
@require_http_methods(["DELETE"])
def delete(request, blog_entry):
    blog_entry.delete()
    return HttpResponseRedirect(urlresolvers.reverse('skram.views.index'))

@require_http_methods(["GET", "POST", "DELETE"])
def blog_entry(request, blog_title):
    blog_entry = models.BlogEntry.get_by_key_name(blog_title)
    if blog_entry is None:
        raise ObjectDoesNotExist('Blog entry %s does not exist!' % blog_title)

    if request.method == 'GET': 
        return read(request, blog_entry)
    if request.method == 'POST':
        return create_or_update(request, blog_entry)
    if request.method == 'DELETE':
        return delete(request, blog_entry)

@openid_login_required(openidgae.models.USERTYPE_SCRUMMASTER)
@require_POST
def is_published_update(request, blog_title):
    try:
        blog_entry = models.BlogEntry.get_by_key_name(blog_title)
        if blog_entry is None:
            raise ObjectDoesNotExist('Blog entry does not exist!')
        
        blog_entry.is_published = (request.POST['is_published'] in ['True', 'true'])
        blog_entry.put()
    except Exception, e:
        logging.error('Exception: ' + str(e))
        return HttpResponse(content='Exception: ' + str(e), status=400)
    
    return HttpResponse(content='200 ok', status=200)

@openid_login_required(openidgae.models.USERTYPE_USER)
@require_POST
def create_comment(request, blog_title):
    try:
        blog_entry = models.BlogEntry.get_by_key_name(blog_title)
        if blog_entry is None:
            raise ObjectDoesNotExist('Blog entry does not exist!')
        
        if not blog_entry.comments_allowed:
            return HttpResponse(content='Commenting is not allowed!', status=403)
        
        blog_comment = models.Comment(text = request.POST['blog-comment'],
                                      blog_entry = blog_entry,
                                      created_by = openidgae.get_current_person(request, HttpResponse()))
        blog_comment.put()
    except Exception, e:
        logging.error('Exception: ' + str(e))
        return HttpResponse(content='Exception: ' + str(e), status=400)
    
    payload = dict(blog_comment=blog_comment)
    snippet_response = skram.views.render(request, HttpResponse(), 'blog_comment_snippet.html', payload)

    return HttpResponse(content=snippet_response.content, status=200)

@openid_login_required(openidgae.models.USERTYPE_USER)
@require_http_methods(["DELETE"])
def delete_blog_comment(request, blog_title, comment_id):
    try:
        blog_comment = models.Comment.get_by_id(int(comment_id));
        if blog_comment is None:
            raise ObjectDoesNotExist('Blog comment does not exist!')
        if blog_comment.created_by.key() != openidgae.get_current_person(request, HttpResponse()).key():
            return HttpResponse(content='Unauthorized user!', status=403)
        blog_comment.delete()
    except Exception, e:
        logging.error('Exception: ' + str(e))
        return HttpResponse(content='Exception: ' + str(e), status=400)
    
    return HttpResponse(content='200 ok', status=200)

@openid_login_required(openidgae.models.USERTYPE_SCRUMMASTER)
@require_POST
def comment_is_spam(request, blog_title, comment_id):
    try:
        blog_comment = models.Comment.get_by_id(int(comment_id));
        if blog_comment is None:
            raise ObjectDoesNotExist('Blog comment does not exist!')
        
        blog_comment.is_spam = (request.POST['is_spam'] in ['True', 'true'])
        blog_comment.put()
    except Exception, e:
        logging.error('Exception: ' + str(e))
        return HttpResponse(content='Exception: ' + str(e), status=400)
    
    return HttpResponse(content='200 ok', status=200)
