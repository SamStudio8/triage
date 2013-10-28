from django.conf.urls import patterns, url
import task.views as TaskViews

urlpatterns = patterns('',
    url(r'^$', TaskViews.list_tasks, name="list_tasks"),
    url(r'^add/(?P<tasklist_id>\w+)/$', TaskViews.add_task, name="add_task"),
    url(r'^edit/(?P<task_id>\w+)/$', TaskViews.edit_task, name="edit_task"),

    url(r'^addlist/$', TaskViews.add_tasklist, name="add_tasklist"),
)
