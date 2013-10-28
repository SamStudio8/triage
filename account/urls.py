from django.conf.urls import patterns, url
from django.contrib.auth.views import login, logout

urlpatterns = patterns('',
    url(r'^login/$', login, {'template_name':'account/login.html'}, name='login'),
    url(r'^logout/$', logout, {'next_page': '/'}, name='logout'),
)
