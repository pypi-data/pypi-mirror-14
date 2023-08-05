# -*- coding: utf-8 -*-
from django import template
from django.db.models import Q
from settings.templatetags.nepali import nepali


register = template.Library()


@register.filter(name='getFormattedPermissions')
def getFormattedPermissions(value):
    from settings.models import config
    if len(value) == 0:
        return config.text.get('no_permissions', "")
    else:
        return u' '.join([
            u'<span class="label label-primary">{}</span>'.format(nepali(_.name)) for _ in value
            ])


@register.filter(name="getReasonablePermissions")
def getReasonablePermission(value):
    return value.permissions.filter(Q(codename__contains="ModUser") | Q(codename__contains="Book"))


@register.filter(name="makeGlyphicon")
def makeGlyphicons(value):
    value = str(value)
    if value.isdigit():
        temp = '<span class="glyphicon glyphicon-{}"></span>'
        return temp.format(value)
    else:
        return ""


@register.filter(name="hasPerm")
def hasPerm(value, arg):
    '''
    check has perm for users
    '''
    return int(value.has_perm(arg))

@register.filter(name="gHasPerm")
def gHasPerm(value, arg):
    '''
    check hasPerm for groups
    '''
    return len(value.permissions.filter(codename=arg)) > 0
