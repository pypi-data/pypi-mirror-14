# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url

urlpatterns = [
    url(r'^search/member/$', 'account.views.search_member', name="search-member"),
    url(r'^login/$', 'account.views.login_user', name="login"),
    url(r'^register/person/$', 'account.views.addWorker', name="addWorker"),
    url(r'^register/person/new/(?P<created>.*)$', 'account.views.addWorkerWithArgs', name="addWorkerWithArgs"),
    url(r'^register/member/$', 'account.views.addMember', name="addMember"),
    url(r'^register/member/new/(?P<created>.*)$', 'account.views.addMemberWithArgs', name="addMemberWithArgs"),
    url(r'^logout/', 'account.views.logout_user', name="logout"),
    url(r'^user/(?P<username>.+)/$', 'account.views.profile', name='profile'),
    url(r'^verifySchool/(?P<userName>.+)/$', 'account.views.verifySchool', name='verifySchool'),
        ]
