# -*- coding: utf-8 -*-
"""sysmanager URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^$', 'head.views.home', name="home"),
    url(r'^head/', include('head.urls')),
    url(r'^user/', include('account.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('ledger.urls')),
    url(r'^groups/', include('almsGroups.urls')),
    url(r'^booktool/', include('booktool.urls')),
    url(r'^spreadsheet/', include('spreadsheet.urls')),
    url(r'^rst/', include('restructuredText.urls')),
    url(r'^miscfields/', include('miscFields.urls')),
    url(r'^settings/', include('settings.urls')),
]
