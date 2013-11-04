from django.conf.urls import patterns, url
import task.views as TaskViews

urlpatterns = patterns('',
    url(r'^list/$', TaskViews.add_tasklist, name="add_tasklist"),
    url(r'^list/(?P<tasklist_id>\w+)/$', TaskViews.edit_tasklist, name="edit_tasklist"),

    url(r'^add/$', TaskViews.add_task, name="add_task"),
    url(r'^add/(?P<tasklist_id>\w+)/$', TaskViews.add_task, name="add_task"),
    url(r'^edit/(?P<task_id>\w+)/$', TaskViews.edit_task, name="edit_task"),
    url(r'^complete/(?P<task_id>\w+)/$', TaskViews.complete_task, name="complete_task"),
)
