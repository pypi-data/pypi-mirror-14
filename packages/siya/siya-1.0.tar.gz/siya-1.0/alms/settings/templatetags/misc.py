# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django import template


register = template.Library()


@register.filter(name="mod")
def mod(value, arg):
    '''
    return modof a number to another
    '''
#   config = Globals()
#   out = ""
#   value = unicode(value)
#   for _ in value:
#       if _ in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']:
#           out += config.text[_]
#       else:
#           out += _
#   return out
    return int(value) % int(arg)
