# -*- coding: utf-8 -*-


from django.conf.urls import url

urlpatterns = [
    url(r'^addNewField$', 'miscFields.views.addNewField', name="addNewField"),
    url(r'^$', 'miscFields.views.home', name="miscFieldsHome"),
    url(r'^editField/(?P<field_id>[0-9]+)$', 'miscFields.views.edit_field', name="miscFieldsEdit"),
    url(r'^deleteField/(?P<field_id>[0-9]+)$', 'miscFields.views.delete_field', name="miscFieldsDelete"),
        ]
