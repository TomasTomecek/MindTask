# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r"^$", "tasks.views.task_list",
        name="tasks/list"),
    url(r"^(?P<stream_name>\w+)/$", "tasks.views.task_list",
        name="tasks/list/stream"),
    url(r"^(?P<stream_name>\w+)/(?P<mmap>\w+)/$", "tasks.views.task_list",
        name="tasks/list/stream/mmap"),
    url(r"^(?P<stream_name>\w+)/(?P<mmap>\w+)/(?P<sheet>\w+)/$", "tasks.views.task_list",
        name="tasks/list/stream/mmap/sheet"),
    url(r"^(?P<stream_name>\w+)/(?P<mmap>\w+)/(?P<sheet>\w+)/(?P<order_by>\w+)/$",
        "tasks.views.task_list",
        name="tasks/list/stream/order_by"),
    url(r"^(?P<stream_name>\w+)/(?P<mmap>\w+)/(?P<sheet>\w+)/(?P<order_by>\w+)/(?P<order>\w+)/$",
        "tasks.views.task_list",
        name="tasks/list/stream/order_by/order"),
)