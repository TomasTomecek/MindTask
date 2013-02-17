# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r"^client/", "kobo.django.xmlrpc.views.client_handler",
        name="help/xmlrpc/client"),
)

