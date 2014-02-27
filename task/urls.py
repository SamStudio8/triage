from django.conf.urls import patterns, url

import receivers

import task.views as TaskViews

urlpatterns = patterns('',
    url(r'^dashboard/$', TaskViews.dashboard, name="dashboard"),
    url(r'^calendar/$', TaskViews.calendar, name="calendar"),

    url(r'^(?P<username>\w+)/task/(?P<task_id>\d+)/$', TaskViews.view_task, name="view_task"),
    url(r'^(?P<username>\w+)/task/(?P<task_id>\d+)/edit/$', TaskViews.edit_task, name="edit_task"),
    url(r'^(?P<username>\w+)/task/(?P<task_id>\d+)/link/$', TaskViews.link_task, name="link_task"),
    url(r'^(?P<username>\w+)/task/(?P<task_id>\d+)/complete/$', TaskViews.complete_task, name="complete_task"),
    url(r'^(?P<username>\w+)/task/new/$', TaskViews.new_task, name="new_task"),


    url(r'^(?P<username>\w+)/settings/triage/new/$', TaskViews.add_triage_category, name="add_triage_category"),
    url(r'^(?P<username>\w+)/settings/triage/(?P<triage_category_id>\d+)/edit/$', TaskViews.edit_triage_category, name="edit_triage_category"),
    url(r'^(?P<username>\w+)/settings/triage/$', TaskViews.list_triage_category, name="list_triage_category"),

    url(r'^(?P<username>\w+)/list/new/$', TaskViews.add_tasklist, name="add_tasklist"),
    url(r'^(?P<username>\w+)/(?P<listslug>[-\w]+)/edit/$', TaskViews.edit_tasklist, name="edit_tasklist"),
    url(r'^(?P<username>\w+)/(?P<listslug>[-\w]+)/delete/$', TaskViews.delete_tasklist, name="delete_tasklist"),
    url(r'^(?P<username>\w+)/(?P<listslug>[-\w]+)/milestones/$', TaskViews.list_milestones, name="list_milestones"),
    url(r'^(?P<username>\w+)/(?P<listslug>[-\w]+)/milestones/(?P<milestone_id>\d+)/$', TaskViews.view_milestone, name="view_milestone"),
    url(r'^(?P<username>\w+)/(?P<listslug>[-\w]+)/milestones/new/$', TaskViews.new_milestone, name="new_milestone"),
    url(r'^(?P<username>\w+)/(?P<listslug>[-\w]+)/milestones/(?P<milestone_id>\d+)/edit/$', TaskViews.edit_milestone, name="edit_milestone"),
    url(r'^(?P<username>\w+)/(?P<listslug>[-\w]+)/$', TaskViews.view_tasklist, name="view_tasklist"),

    url(r'^(?P<username>\w+)/$', TaskViews.profile, name="profile"),
)
