# -*- coding: utf-8 -*-
'''

    / ___|__ _ _ __    _   _  ___  _   _   ___  ___  ___  | |
   | |   / _` | '_ \  | | | |/ _ \| | | | / __|/ _ \/ _ \ | '_ \ / _ \ '__|
   | |__| (_| | | | | | |_| | (_) | |_| | \__ \  __/  __/ | | | |  __/ |
    \____\__,_|_| |_|  \__, |\___/ \__,_| |___/\___|\___| |_| |_|\___|_|
                        |___/

                                 | |_ ___   ___|__ \
                                 | __/ _ \ / _ \ / /
                                 | || (_) | (_) |_|
                                  \__\___/ \___/(_)
'''


from django.db import models

# Create your models here.


class Theme:
    '''
    The Theme class defines the color pallete to be used for the website
    '''
    pass


# configurations on an organizational level
# everyone in the organizaation must abide to these configurations
# these can only be changed by the admin(s)
class Organization(models.Model):

    # name of the organization
    full_name = models.TextField(default="Hami Sabai Ko Library")
    short_name = models.CharField(default="HSKL", max_length=100)

    # slogan of the org.
    motto = models.TextField(default="Reading Is Fun!")
    # extra configuration for the whole library to follow

    late_fees_rate = models.IntegerField(default=2)

    # maximum number of days to let borrow a book
    max_days_borrow = models.IntegerField(default=10)

    # maximum number of books a member can borrow at once
    max_books_borrow = models.IntegerField(default=2)

    # time period of reports
    time_period_report = models.IntegerField(default=3)  # in months

    '''
    ## Does the library have a theme of the month?
    has_theme_of_month = models.BooleanField(default=False)

    ## If the library has a theme of the month, what is it?
    theme_of_the_month = models.ForeignKey(Theme,null=True)
    '''
