# -*- coding: utf-8 -*-
from django import template
from django.db import models
from django.core.exceptions import ObjectDoesNotExist

from miscFields.models import GenericField
from settings.models import Globals


from pyBSDate.BSDate import convert_to_bs

register = template.Library()

NONE_LS = [None, "None"]


@register.filter(name="tobs")
def to_bs(value):
    return convert_to_bs(value)


@register.filter(name="get_obj")
def get_obj(value, arg):
    return value.eval()


@register.filter(name="getBookValue")
def getBookValue(value, arg):
    '''
    The value is a Book class
    '''
    if value not in NONE_LS:
        # is the arg starts with __gen_,
        # it is a key for the GenericField class and isn't directly
        # affiliated to the Book class
        if arg.startswith("__gen_"):
            gf = GenericField.objects.get(key=arg[6:])
            try:  # if the book does not have value for that field, return ""
                value = gf.value.get(book=value).value
            except ObjectDoesNotExist:
                value = ""
            return value
        if arg == 'call_no':
            return value.get_call_number()
        elif arg == 'auth':
            return value.get_authors()
        elif arg == 'title':
            return value.get_title()
        elif arg == 'pub_place':
            return value.publisher.get_place()
        elif arg == 'pub_name':
            return value.publisher.get_name()
        elif arg == 'pub_year':
            return value.publisher.get_year()
        elif arg == 'no_of_pages':
            if value.no_of_pages not in NONE_LS:
                return value.no_of_pages
        elif arg == 'price':
            if value.price not in NONE_LS:
                return value.price
        elif arg == 'ser':
            if value.series not in NONE_LS:
                return value.series
        elif arg == 'isbn':
            if value.isbn not in NONE_LS:
                return value.isbn
        elif arg == 'edtn':
            if value.edition not in NONE_LS:
                return value.edition
        elif arg == 'vol':
            if value.volume not in NONE_LS:
                return value.volume
        elif arg == 'acc_no':
            return value.get_accession_number()
        elif arg == 'kwds':
            return value.get_keywords()
        elif arg == 'gftd_name':
            if value.gifted_by is None:
                return ""
            else:
                return value.gifted_by.get_name()
        elif arg == 'gftd_phn':
            if value.gifted_by is None:
                return ''
            else:
                return value.gifted_by.get_phone_no()
        elif arg == "gftd_email":
            if value.gifted_by is None:
                return ''
            else:
                return value.gifted_by.get_email()
    return ""
