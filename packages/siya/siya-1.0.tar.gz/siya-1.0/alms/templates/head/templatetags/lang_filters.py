# -*- coding: utf-8 -*-
from django import template

register = template.Library()


@register.filter(name="nepali")
def num_preeti(value):
    SHEET = {
                ')': 0,
                '!': 1,
                '@': 2,
                '#': 3,
                '$': 4,
                '%': 5,
                '^': 6,
                '&': 7,
                '*': 8,
                '(': 9
            }
    return "".join([SHEET.get(_, "") for _ in value if _.isdigit() == True])
