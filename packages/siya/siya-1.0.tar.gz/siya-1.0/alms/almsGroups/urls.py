# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url

urlpatterns = [
            url(r'^(?P<group_added>[01]+)/(?P<group_name>.+)/$', 'almsGroups.views.homeWithArgs',name="almsGroupsHomeWithArgs"),
            url(r'^$', 'almsGroups.views.home',name="almsGroupsHome"),
            url(r'^add/$', 'almsGroups.views.addGroup',name="addNewGroup"),
            url(r'^edit/(?P<group_id>[0-9]+)$', 'almsGroups.views.editGroup',name="editGroup"),
            url(r'^delete/(?P<group_id>[0-9]+)$', 'almsGroups.views.deleteGroup',name="deleteGroup"),
        ]
