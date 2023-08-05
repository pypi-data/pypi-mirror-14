# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url

urlpatterns = [
            url(r'^create/$', 'restructuredText.views.writeHomeBody',name="writeHomeBody"),
        ]
