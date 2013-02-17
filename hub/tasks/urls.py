# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r"^$", "tasks.views.task_list_in_progress", name="tasks/list"),
    url(r"^completed/$", "tasks.views.task_list_completed",
        name="tasks/list/completed"),
    url(r"^in_progress/$", "tasks.views.task_list_in_progress",
        name="tasks/list/in_progress"),
)