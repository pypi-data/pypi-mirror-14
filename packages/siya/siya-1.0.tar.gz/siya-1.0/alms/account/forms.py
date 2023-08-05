# -*- coding: utf-8 -*-
from django import forms
from django.contrib.admin import widgets

from settings.models import Globals

config = Globals()

from django.contrib.auth.models import Group


class CreateMemberForm(forms.Form):
    first_name = forms.CharField(label="First Name")
    last_name = forms.CharField(label="Last Name")
    gender = forms.ChoiceField(label="Gender", choices=(("female", config.text['female']), ('male', config.text['male'])))
    ward_no = forms.CharField(label="Ward No.")
    tole = forms.CharField(label="Tole")
    city = forms.CharField(label="City")
    home_phone = forms.CharField(label="Home Phone No.")
    parent_name = forms.CharField(label="Parent's Name")
    school_name = forms.CharField(label="School Name")
    school_class = forms.CharField(label="Class")
    roll_no = forms.CharField(label="Roll No.")
    date_of_birth = forms.DateTimeField(widget=widgets.AdminDateWidget(), label="Date Of Birth")


def getAllGroups():
    out = []
    for grp in Group.objects.all():
        out.append(((grp.name), (grp.name)))
    return out


class CreateWorkerForm(forms.Form):
    first_name = forms.CharField(label="First Name")
    last_name = forms.CharField(label="Last Name")
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    gender = forms.ChoiceField(label="Gender", choices=(("female", config.text['female']), ('male', config.text['male'])))
    date_of_birth = forms.DateTimeField(widget=widgets.AdminDateWidget(), label="Date Of Birth")
    group = forms.ChoiceField(label="Group", choices=getAllGroups())
