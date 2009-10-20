from django.conf.urls.defaults import *

urlpatterns = patterns('skram.blog.views',
    (r'^$', 'create_or_update'),
    (r'^(?P<blog_title>[^\.^/]+)$', 'blog_entry'),
    (r'^(?P<blog_title>[^\.^/]+)/is_published$', 'is_published_update'),
    (r'^(?P<blog_title>[^\.^/]+)/comments$', 'create_comment'),
    (r'^(?P<blog_title>[^\.^/]+)/comments/(?P<comment_id>[^\.^/]+)$', 'delete_blog_comment'),
    (r'^(?P<blog_title>[^\.^/]+)/comments/(?P<comment_id>[^\.^/]+)/is_spam$', 'comment_is_spam'),
)