from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^$', 'skram.views.index'),
    (r'^kaj-je-skram$', 'skram.views.about_scrum'),
    (r'^poll/create/$', 'skram.poll.views.create'),
    (r'^poll/(?P<poll_key>[^\.^/]+)/$', 'skram.poll.views.poll_detail'),
    (r'^poll/(?P<poll_key>[^\.^/]+)/results/$', 'skram.poll.views.poll_results'),
    (r'^poll/(?P<poll_key>[^\.^/]+)/delete/$', 'skram.poll.views.delete'),
    (r'^mojster-skrama$', 'skram.scrummaster.views.index'),
    (r'^lastnik-produkta$', 'skram.product_owner.views.index'),
    (r'^mostvo$', 'skram.team.views.index'),
    (r'^uporabniki/(?P<openID>\S+)/usertype/(?P<userType>\d)$', 'skram.users.views.usertype_update'),
    (r'^uporabniki$', 'skram.users.views.index'),
    (r'^twitter-status-update$', 'skram.views.twitter_status_update'),
    (r'^log_me_in$', 'skram.poll.views.log_me_in'),
    (r'^openid/', include('openidgae.urls')),
    (r'^blog-entries/', include('skram.blog.urls')),
)