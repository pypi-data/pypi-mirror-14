__author__ = 'sushil'
from utilities import decompose_date, validate_date_bs, validate_date_ad
from utilities import _bs_to_ad, _ad_to_bs

from sys import argv
import datetime


def convert_to_ad(bs_date):
    date_components = decompose_date(bs_date)
    year, month, day = date_components
    validate_date_bs(year, month, day)

    ad_year, ad_month, ad_day = _bs_to_ad(year, month, day)
    return "{}-{}-{}".format(ad_year, ad_month, ad_day)


def convert_to_bs(ad_date):
    date_components = decompose_date(ad_date)
    year, month, day = date_components
    validate_date_ad(year, month, day)

    bs_year, bs_month, bs_day = _ad_to_bs(year, month, day)
    return "{}-{}-{}".format(bs_year, bs_month, bs_day)
