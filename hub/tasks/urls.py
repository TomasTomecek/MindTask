# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r"^$", "tasks.views.task_list",
        kwargs={"stream_name":"active",
                "order_by": "progress",
                "order": "up",},
        name="tasks/list"),
    url(r"^(?P<stream_name>\w+)/$", "tasks.views.task_list",
        kwargs={"order_by": "progress",
                "order": "up",},
        name="tasks/list/stream"),
    url(r"^(?P<stream_name>\w+)/(?P<order_by>\w+)/$", "tasks.views.task_list",
        kwargs={"order": "up",},
        name="tasks/list/stream/order_by"),
    url(r"^(?P<stream_name>\w+)/(?P<order_by>\w+)/(?P<order>\w+)/$", "tasks.views.task_list",
        name="tasks/list/stream/order_by"),
)