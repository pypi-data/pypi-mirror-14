# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django import template


from settings.models import Globals

from pyBSDate.BSDate import convert_to_bs
from settings.templatetags.nepali import nepali

import datetime

register = template.Library()

NONE_LS = [None, "None"]

config = Globals()


@register.filter(name="tobs")
def to_bs(value):
    if value.__class__ not in [unicode, str] and value is not None:
        try:
            print value.__class__
            if value.__class__ is datetime.datetime:
                value = value.date()
            value = value.isoformat()
        except:
            raise TypeError("value doesn't have isoformat method")
    elif value.__class__ is datetime.datetime:
        to_bs(value.date())
    elif value is None:
        return ""
    value = value.replace("-", "/")
    np_date = convert_to_bs(value)
    return np_date


@register.filter(name="pdate")
def pdate(value):
    '''
    pretty nepali date format from str
    '''
    vals = value.split("-")
    if len(vals) == 3:
        return "{} {} {}".format(vals[0], config.text.get("m"+str(int(vals[1]))), nepali(vals[2]))
