# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

urlpatterns = [
            url(r'^journal/$', 'ledger.views.journalHome',name='journalHome'),
            url(r'^addCredit/$', 'ledger.views.addCredit',name='addCredit'),
            url(r'^addDebit/$', 'ledger.views.addDebit',name='addDebit'),
            url(r'^addEntry/$', 'ledger.views.addOneDaysEntry',name='addOneDaysEntry'),
            url(r'^journal/(?P<year>[0-9]+)/(?P<month>[0-9]+)/$', 'ledger.views.showJournal',name="showJournal"),
        ]
