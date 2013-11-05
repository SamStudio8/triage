from django.conf.urls import patterns, url
import task.views as TaskViews

urlpatterns = patterns('',
    url(r'^list/$', TaskViews.add_tasklist, name="add_tasklist"),
    url(r'^list/(?P<tasklist_id>\w+)/$', TaskViews.edit_tasklist, name="edit_tasklist"),

    url(r'^add/$', TaskViews.add_task, name="add_task"),
    url(r'^add/(?P<tasklist_id>\w+)/$', TaskViews.add_task, name="add_task"),
    url(r'^edit/(?P<task_id>\w+)/$', TaskViews.edit_task, name="edit_task"),
    url(r'^complete/(?P<task_id>\w+)/$', TaskViews.complete_task, name="complete_task"),

    url(r'^category/$', TaskViews.list_task_triages, name="list_task_triages"),
    url(r'^category/add/$', TaskViews.add_triage_category, name="add_triage_category"),
    url(r'^category/edit/(?P<triage_category_id>\w+)$', TaskViews.edit_triage_category, name="edit_triage_category"),
)
