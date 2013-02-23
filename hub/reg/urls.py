# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^login/$',
        'django.contrib.auth.views.login',
        {'template_name': 'registration/login.html'},
        name="reg/login"),
    url(r'^logout/$',
        'django.contrib.auth.views.logout',
        kwargs={'next_page':'/registration/login'},
        name="reg/logout"),
)