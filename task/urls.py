from django.conf.urls import patterns, url
import task.views as TaskViews

urlpatterns = patterns('',
    url(r'^dashboard/$', TaskViews.dashboard, name="dashboard"),

    url(r'^(?P<username>\w+)/task/(?P<task_id>\d+)/', TaskViews.view_task, name="view_task"),

    url(r'^tasklist/new/$', TaskViews.add_tasklist, name="add_tasklist"),
    url(r'^tasklist/(?P<tasklist_id>\d+)/edit/$', TaskViews.edit_tasklist, name="edit_tasklist"),
    url(r'^tasklist/(?P<tasklist_id>\d+)/task/new/$', TaskViews.add_task, name="add_task"),

    url(r'^task/(?P<task_id>\d+)/$', TaskViews.view_task, name="view_task"),
    url(r'^task/new/$', TaskViews.add_task, name="add_task"),
    url(r'^task/(?P<task_id>\d+)/edit/$', TaskViews.edit_task, name="edit_task"),
    url(r'^task/(?P<task_id>\d+)/complete/$', TaskViews.complete_task, name="complete_task"),
    url(r'^task/(?P<task_id>\d+)/link/$', TaskViews.link_task, name="link_task"),

    url(r'^category/$', TaskViews.list_triage_category, name="list_triage_category"),
    url(r'^category/new/$', TaskViews.add_triage_category, name="add_triage_category"),
    url(r'^category/(?P<triage_category_id>\d+)/edit/$', TaskViews.edit_triage_category, name="edit_triage_category"),

)
