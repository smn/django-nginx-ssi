from django.conf.urls.defaults import *
from ssi.views import render_from_cache

urlpatterns = patterns('',
    (r'^(.*)/$', render_from_cache, {}, 'nginxssi'),
)
