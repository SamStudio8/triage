from django.conf.urls import patterns, include, url
from task import views as TaskViews

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', TaskViews.list_tasks, name="home"),
    url(r'^task/', include("task.urls", namespace="task", app_name="task")),
    url(r'^account/', include("account.urls", namespace="account", app_name="account")),
)
