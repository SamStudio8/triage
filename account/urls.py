from django.conf.urls import patterns, url
from django.contrib.auth.views import (login, logout, password_reset,
        password_reset_done, password_reset_confirm, password_reset_complete)

from account import views

urlpatterns = patterns('',
    #TODO Disable Registration Setting
    url(r'^register/$', views.register, name="register"),
    url(r'^login/$', login, {'template_name':'login.html'}, name='login'),
    url(r'^logout/$', logout, {'next_page': '/'}, name='logout'),

    url(r'^password/reset/(?P<uidb36>.+)/(?P<token>.+)/$', password_reset_confirm,
           {"template_name": "reset_conf.html",
            "current_app": "account",
            "post_reset_redirect": "/account/password/complete/"},
        name="password_reset_confirm"),
    url(r'^password/reset/$', password_reset, 
           {"template_name": "reset.html",
            "email_template_name": "reset_mail.html",
            "subject_template_name": "reset_subject.txt",
            "current_app": "account",
            "from_email": "triage@ironowl.io", #TODO Import email address
            "post_reset_redirect": "/account/password/sent/"},
        name="reset"),
    url(r'^password/sent/$', password_reset_done, {"template_name": "reset_ok.html"}, name="password_done"),
    url(r'^password/complete/$', password_reset_complete, {"template_name": "reset_complete.html"}, name="password_complete"),
)
