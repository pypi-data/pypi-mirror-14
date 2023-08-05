# -*- coding: utf-8 -*-
from django import template
from django.db import models

register = template.Library()

NONE_LS = [None,"None"]

@register.filter(name="addSmilies")
def addSmilies(value):
    '''
    The value is a Book class
    '''
    smileys = {
            ":)":"smiley",
            "^-^":"azn",
            "^_^": "azn",
            ":*": "angry",
            ";)": "wink",
            ":P": "tongue",
            ":O": "shocked",
            ":0": "shocked",
            "<3": "kiss",
            "B)": "cool",
            "BD": "cool",
            "O)": "angel",
            "OD": "angel",
            ":D": "laugh",
            }
    for _ in smileys.items():
        value = value.replace(_[0], '<img class="smiley" src="/static/smileys/{}.gif">'.format(_[1]))
    return value
