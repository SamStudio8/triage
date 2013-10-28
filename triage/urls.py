from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^account/', include("account.urls", namespace="account", app_name="account")),
    url(r'^task/', include("task.urls", namespace="task", app_name="task")),
)
