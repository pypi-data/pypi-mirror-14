# -*- coding: utf-8 -*-


from django.conf.urls import patterns, url

urlpatterns = [
            url(r'^$', 'settings.views.home',name="settingsHome"),
        ]
