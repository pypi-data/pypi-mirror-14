# -*- coding: utf-8 -*-
from django import template

register = template.Library()


@register.filter(name="strfdate")
def strftime(value, arg):
    return value.strftime(arg)
