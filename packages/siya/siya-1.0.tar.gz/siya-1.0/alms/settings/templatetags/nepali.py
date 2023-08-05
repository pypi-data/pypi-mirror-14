# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django import template

import string

from settings.models import Globals

from head.templatetags.bookFilters import to_bs

import datetime

register = template.Library()


@register.filter(name="no_to_np")
def no_to_np(value):
    '''
    convert number to nepali
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
    return value


@register.filter(name="nepali")
def nepali(value):
    '''
    try to convert text to nepali
    '''
    if value is not None:
        if value.__class__ == datetime.date:
            return no_to_np(to_bs(value.isoformat()))
        config = Globals()
        raw_value = value
        value = value.lower().replace(" ", "_")
        out_val = ""
        for _ in value:
            if _ in string.ascii_lowercase + string.ascii_uppercase or _ == "_":
                out_val += _
        while len(out_val) > 1 and out_val[0] not in string.ascii_lowercase + string.ascii_uppercase + "".join([unicode(_) for _ in range(0, 10)]):
            out_val = out_val[1:]

        text = config.text.get(out_val, None)
        if text is not None:  # found the text correspondent
            return text
        else:
            values = raw_value.split(" ")
            out_val = []
            for _ in values:
                _ = "".join([char for char in _ if char in string.ascii_lowercase+string.ascii_uppercase+"".join([unicode(int) for int in range(0,10)]) or _ == " "])
                config_val = config.text.get(_, None)
                if config_val is None:
                    config_val = config.text.get(_.lower(), None)
                    if config_val is None:
                        out_val.append(_)
                    else:
                        out_val.append(config_val)
                else:
                    out_val.append(config_val)
            return " ".join(out_val)
    else:
        return ""


