# -*- coding: utf-8 -*-
#
#  ____             _   _       ___       ____            _
# |  _ \  ___  __ _| |_| |__   |_ _|___  |  _ \ ___  __ _| |
# | | | |/ _ \/ _` | __| '_ \   | |/ __| | |_) / _ \/ _` | |
# | |_| |  __/ (_| | |_| | | |  | |\__ \ |  _ <  __/ (_| | |
# |____/ \___|\__,_|\__|_| |_| |___|___/ |_| \_\___|\__,_|_|
#
# If you can keep your head when all about you
#    Are losing theirs and blaming it on you,
# If you can trust yourself when all men doubt you,
#    But make allowance for their doubting too;
# If you can wait and not be tired by waiting,
#    Or being lied about, don't deal in lies,
# Or being hated, don't give way to hating,
#    And yet don't look too good, nor talk too wise:
#


from django.db import models
from django.utils.encoding import smart_str
# Create your models here
from account.models import ModUser
from settings.models import Globals
from django.utils import timezone

from miscFields.models import GenericField

import datetime

from pyBSDate.BSDate import convert_to_bs


config = Globals()


def make_title(title):
    title = title.strip(" ")
    return title[0].upper() + title[1:]


NP_NUM = {
    [
        ')',
        '!',
        '@',
        '#',
        '$',
        '%',
        '^',
        '&',
        '*',
        '('][x]: str(x) for x in range(0, 10)
    }


LANG_LIST = [
    'EN',
    'NP'
    ]

CURRENT_LANGUAGE = LANG_LIST[0]


def toint(val, lang="EN"):
    '''
    converts a nepali or english numerical character to integer
    usage : toint(val, [lang])
    '''

    if val is None or val == "None" or val == "":
        return 0
    else:
        if lang.upper() == "NP":
            l = ""
            for char in str(val):
                l += NP_NUM[str(char)]
            return int(l)
        elif lang.upper() == "EN":
            return int(val)
        else:
            return int(val)


def cint(v, b, lang="EN"):
    '''
    like toint, except you can manually specify whether to convert number or
    not.
    usage : cint(v, b, [lang])
    b = To Convert or not
    v = value to convert
    '''

    if b == 0 or b is False:
        return v
    else:
        return toint(v, lang)


class Publisher(models.Model):
    '''
    Model that holds the attributes of a publisher
    Proterties :
        * name
        * place
        * year

    Methods :
        * get_all_attr_for_spreadsheet
        * get_name
        * get_place
        * get_year
        * __str__
        * __catalog__
    '''

    name = models.CharField(max_length=255, db_index=True)
    place = models.CharField(max_length=255, db_index=True)
    year = models.CharField(max_length=10, db_index=True)

    def get_all_attr_for_spreadsheet(self):
        '''
        returns a tuple of tuples containing the following :
            * ("Name", <name of publisher of the object>)
            * ("Place Of Publication", <Place of publication of the object>)
            * ("Year Of Publication", <year of publication of the object>)
        '''
        return (
                    ("Name", self.get_name()),
                    ("Place Of Publication", self.get_place()),
                    ("Year Of Publication", self.get_year())
                )

    def get_name(self):
        '''
        returns the name of the publisher
        '''
        if self.name in [None, "None"]:
            return ""
        return smart_str(self.name).title()

    def get_place(self):
        '''
        returns the placeof publication
        '''
        if self.place in [None, "None"]:
            return ""
        return smart_str(self.place)

    def get_year(self):
        '''
        returns the year of publication
        '''
        if self.year in [None, "None"]:
            return ""
        return smart_str(self.year)

    def get_nepali_year(self):
        if self.year.isdigit():
            year = int(self.year)
        else:
            return self.year
        if year > datetime.datetime.today().year:  # date is in nepali
            return unicode(year)
        else:  # date is in english
            return unicode(year+52) + u' वि.सं'

    def __str__(self):
        '''
        returns a str object for the publisher object.
        If the year is not given, the format is -
          <publisher's name>, <place of publication>
        If the place is not given, the format is -
          <publisher's name> in <year of publication>
        If all the properties are given, the format is -
          <name of publisher>, <place of publication> in <year of publication>

        The name is compulsory for a publisher. If the name is not given,
        nothing is displayed
        '''
        out = u''  # return value
        if self.name == [u"", "", None]:
            out = smart_str("")
        elif (self.year == 0 or self.year == u'0' or self.year.isdigit() is False) and self.place not in [None, 'None'] and self.name not in [None, 'None']:
            out = smart_str(u"{0}, {1}".format(
                self.name,
                self.place))
        elif self.place in [None, 'None'] and self.year not in [None, 'None', '0', 0] and self.name not in [None, 'None']:
            out = smart_str(u"{0} - {1} मा".format(
                self.name,
                self.get_nepali_year()))
        else:
            # fixing a little problem with self.year
            out = smart_str(u"{0}, {1} - {2} मा".format(
                self.name,
                self.place,
                self.get_nepali_year()))
        if out.strip(" ") == ",":  # if the output is only a "," return nothing
            return ""
        return out

    def __catalog__(self):
        if self.year == u"0" and self.place is not None and self.name is not None:
            return smart_str(u"{1}: {0}".format(
                self.name,
                self.place))
        elif self.place is None and self.year is not None and self.name is not None:
            return smart_str(u"{0}: {1}".format(
                self.name,
                self.year))
        else:
            return smart_str(u"{1}: {0}: {2}".format(
                self.name,
                self.place,
                self.year))


class Author(models.Model):
    '''
    Model for Author Class
    Properties :
        * name
        * slug
    Methods :
        * get_all_attr_for_spreadsheet
        * get_name
        * get_catalog_name
        * __str__
    '''
    name = models.CharField(max_length=100)
    slug = models.SlugField(db_index=True)

    def get_all_attr_for_spreadsheet(self):
        return (
            ("Name", self.get_name()),
            )

    def get_name(self):
        '''
        the data entered for an author is in the format:
        <first name> <last name>
        '''
        if self.name in [None, "None"]:
            return ""
        name_list = self.name.split(",")
        name_list.reverse()
        if len(name_list) == 2:
            joiner = u" "  # joins 2 author names
        else:
            joiner = u", "   # joins more than 2 author names
        return joiner.join(name_list)

    def get_catalog_name(self):
        '''
        returns the traditional style author name. It's format is:
            <last name>, <first_name>
        '''
        name_list = self.name.split(",")
        if name_list.__len__() >= 2:
            return self.name
        elif len(name_list) == 1:
            return ",".join(name_list[0].split(" "))

    def __str__(self):
        '''
        returns the name of the author
        '''
        return smart_str(self.name)


class KeyWord(models.Model):
    '''
    The Keyword Model for Book class.
    It has a ManyToMany relationship with Book.
    synonymn to tags.

    properties :
        * name
        * slug
    methods :
        * __str__
    '''
    name = models.CharField(max_length=255)
    slug = models.SlugField(db_index=True)

    def __str__(self):
        '''
        returns the name of the keyword as a title
        '''
        return smart_str(self.name.title())


class Lend(models.Model):
    '''
    Abstract object that works with the lending and borrowing of books.
    Properties :
        * user
        * book
        * lending_date
        * returned_date
        * returned
        * borrowed
    Methods :
        * get_all_attr_for_spreadsheet
        * get_borrowed_time
        * get_late_fees
        * set_returned
        * get_returning_date
        * __str__
    '''
    user = models.ForeignKey(ModUser, db_index=True)
    book = models.ForeignKey('Book', db_index=True)
    lending_date = models.DateField(db_index=True)
    returned_date = models.DateField(null=True, db_index=True)
    returned = models.BooleanField(default=False, db_index=True)
    borrowed = models.BooleanField(default=False, db_index=True)

    def get_all_attr_for_spreadsheet(self):
        return self.book.get_all_attr_for_spreadsheet() + (
            ("Borrowed By", self.user.username),
            ("Lent Date", self.lending_date)
            )

    def get_borrowed_time(self):
        dt = datetime.date.today() - self.lending_date
        return int(dt.days)

    def get_late_fees(self):
        borrowed_time = self.get_borrowed_time()
        max_days = config.config.getint("books", "borrow_max_days")
        money_per_day = config.config.getint("misc", "late_fees_rate")
        if borrowed_time > max_days:
            return money_per_day * (borrowed_time - max_days)
        else:
            return 0

    def set_returned(self, date=datetime.datetime.today()):
        self.returned_date = date
        self.returned = True
        self.save()
        self.book.state = 0
        self.book.save()

    def get_returning_date(self):
        return self.lending_date + datetime.timedelta(days=config.config.getint("books", 'borrow_max_days'))

    def __str__(self):
        return "{0},borrowed on {1}, till {2}".format(
            str(self.book),
            self.lending_date.strftime("%A %eth %B, %Y"),
            self.get_returning_date().strftime("%A %eth %B, %Y")
            )


class Gifter(models.Model):
    '''
    This class describes the person who gifted this book
    '''
    date_given = models.DateField(auto_now_add=True, db_index=True)
    gifter_name = models.CharField(max_length=255)
    email = models.EmailField(null=True)
    phone = models.IntegerField(null=True)

    def get_email(self):
        if self.email in [None, "None"]:
            return ""
        return smart_str(self.email)

    def get_phone_no(self):
        if self.phone in [None, "None"]:
            return ""
        return smart_str(self.phone)

    def get_name(self):
        return smart_str(self.gifter_name)

    def __str__(self):
        if self.email is None:
            if self.phone is None:
                return "{} on {}".format(self.gifter_name, self.date_given)
            else:
                return "{0}, phone no.: {1} on {2}".format(self.gifter_name, self.phone, self.date_given)
        elif self.phone is None:
            if self.email is None:
                return "{0} on {1}".format(self.gifter_name, self.date_given)

            else:
                return "{0}, email: {1} on {2}".format(self.gifter_name, self.email, self.date_given)
        else:
            return "{0}, phone: {1}, email: {2} on {3}".format(self.gifter_name, self.phone, self.email, self.date_given)


class BookSaver(models.Model):
    '''
    This class represents the Person who modifies/adds a book.
    It stores the user information and datetime of the book added
    '''
    user = models.ForeignKey(ModUser)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{0} on {1}".format(self.user.get_name(), self.date.isoformat())


class Book(models.Model):
    accession_number = models.CharField(max_length=9, db_index=True)
    accessioned_date = models.DateField(auto_now=True, db_index=True)
    '''
    call number describes the type of book, such as - is it a story book?
    Is it a nepali book? english book? Hindi book? Is it fiction? reference?
    etc
    '''
    call_number = models.CharField(max_length=20, null=True, blank=True, db_index=True)
    author = models.ManyToManyField(Author, db_index=True)  # author of the book
    title = models.CharField(max_length=255, db_index=True)    # name of the book
    no_of_pages = models.IntegerField(db_index=True)
    '''
    If the book is part of a series,
    this tells the number in which the book falls into the series
    '''

    # !!!!! language is now obsolete!!!!!!!!!
    language = models.CharField(max_length=5, default="EN", db_index=True)
    # !!!!! language is now obsolete!!!!!!!!!

    publisher = models.ForeignKey(Publisher, null=True, blank=True, db_index=True)
    series = models.CharField(max_length=20, blank=True, null=True, db_index=True)
    edition = models.CharField(max_length=100, blank=True, null=True, db_index=True)
    price = models.CharField(max_length=255, null=True, blank=True, db_index=True)
    volume = models.CharField(max_length=10, null=True, blank=True, db_index=True)
    keywords = models.ManyToManyField(KeyWord, db_index=True)

    isbn = models.CharField(max_length=13, null=True, db_index=True)
    '''
    State has three values:
    0 - Is available
    1 - Is Discarded
    2 - Is borrowed
    defaults to {0}
    '''
    state = models.IntegerField(default=0, db_index=True)
    '''
    The keywords describe in a more specific manner, the "personality" of the
    book which the call number failed to explain
    '''
    gifted_by = models.ForeignKey(Gifter, null=True, db_index=True)
    saved_by = models.ManyToManyField(BookSaver, default=timezone.now,  db_index=True)

    def bring_back(self):
        '''
        यदि किताब खारेज गरीएको छ भने फिर्ता ल्याउने
        '''
        if self.state != 0:
            self.state = 0
            self.save()
        return 0

    def discard(self):
        '''
        किताब खारेज गर्ने
        '''
        self.state = 1
        self.save()

    def is_discarded(self):
        '''
        किताब खारेज गरिएको छ कि छैन
        '''
        return self.state == 1

    @staticmethod
    def get_attr_list():
        '''
        सबै गुणहरु सूची गर्ने
        अप्रचलित तरिका!!!!!!
        '''
        return (
            'accNo',
            'callNo',
            'title',
            'author',
            'publisher',
            'no_of_pages',
            'keywords',
            'date_added'
        )

    def get_all_attr(self):
        '''
        किताब instanceका सबै गुणहरु सूची गर्ने

        ढाँचा : 

            (
                (<name of attribute>, <value of attribute for this instance>),
                ...
                ...
            )
        '''
        return (
            ('Accession Number', self.accession_number),
            ('Call Number', smart_str(self.call_number)),
            ('Title', smart_str(self.title)),
            ('Author', self.get_authors()),
            ('Publisher', self.get_publishers()),
            ('No. of Pages', self.no_of_pages),
            ('keywords', smart_str(self.get_keywords())),
            ('Date Added', self.accessioned_date),
            ("Series", self.get_series()),
            ("Edition", self.get_edition()),
            ("Price", self.get_price()),
            ("Volume", self.get_volume()),
            ("Gifted By", self.get_gifted_by()),
        )

    def get_all_attr_for_spreadsheet(self):
        '''
        returns all the attributes of the book instance in a pretty format

        format : 

            (
                (<name of attribute>, <value of attribute for this instance>),
                ...
                ...
            )
        '''
        value = (
            ('Accession Number', self.get_accession_number()),
            ('Call Number', self.get_call_number()),
            ('Title', self.get_pretty_title()),
            ('Author', self.get_authors()),
            ('Publisher Name', self.get_publisher_name()),
            ('Year Of Publication', self.get_published_year()),
            ('Place Of Publication', self.get_published_place()),
            ('No. of Pages', self.no_of_pages),
            ('keywords', smart_str(self.get_keywords())),
            ('Date Added', self.accessioned_date),
            ("Series", self.get_pretty_series()),
            ("Edition", self.get_edition()),
            ("Price", self.get_pretty_price()),
            ("Volume", self.get_volume()),
            ("Gifted By", self.get_gifted_by_name()),
            ("Email Of Gifter", self.get_gifted_by_email()),
            ("Phone No. Of Gifter", self.get_gifted_by_phone_no())
        )
        return value

    def get_publisher_name(self):
        '''
        returns name of the publisher or empty string
        '''
        if self.publisher in [None, 'None']:
            return ""
        else:
            return smart_str(self.publisher.get_name())

    def get_published_year(self):
        '''
        returns the year of publication of empty string
        '''
        if self.publisher in [None, 'None']:
            return ""
        else:
            return self.publisher.get_year()

    def get_published_place(self):
        '''
        returns the place of publication or empty string
        '''
        if self.publisher in [None, 'None']:
            return ""
        else:
            return smart_str(self.publisher.get_place())

    def get_gifted_by_name(self):
        '''
        returns the name of person who gifted the book or empty string
        '''
        if self.gifted_by in [None, 'None']:
            return ""
        else:
            return self.gifted_by.get_name()

    def get_gifted_by_email(self):
        '''
        returns the email of person who gifted the book or empty string
        '''
        if self.gifted_by in [None, 'None']:
            return ""
        else:
            return self.gifted_by.get_email()

    def get_gifted_by_phone_no(self):
        '''
        returns the phone number of person who gifted the book or empty string
        '''
        if self.gifted_by in [None, "None"]:
            return ""
        else:
            return self.gifted_by.get_phone_no()

    def get_accession_number(self):
        '''
        returns the accession number of the book. Since the accession number
        is  a required attribute, an empty string is never returned
        '''
        return smart_str(self.accession_number)

    def get_pretty_accession_number(self):
        '''
        returns the accession number
            same as get_accession_number
        '''
        return self.get_accession_number

    def get_call_number(self):
        '''
        returns the call number or empty string
        '''
        if self.call_number in [None, 'None']:
            return ""
        if self.language == "EN":
            return smart_str(self.call_number)
        else:
            call_no = "".join([smart_str(cint(_,_ in NP_NUM.keys(), lang=self.language)) for _ in self.call_number])
            return smart_str(call_no)

    def get_pretty_call_nnumber(self):
        '''
        same as get_call_number
        '''
        return self.get_call_number()

    def get_language(self):
        '''
        returns the langauge of the book.

        Note : language attribute is obsolete
        '''
        if self.language in [None, "None"]:
            return ''
        return smart_str(self.language)

    def get_pretty_language(self):
        '''
        same as get_langauge

        Note : language attribute is obsolete
        '''
        return self.get_language()

    def get_series(self):
        '''
        returns the series of the book or empty string
        '''
        if self.series in [None, "None"]:
            return ""
        else:
            return smart_str(self.series)

    def get_pretty_series(self):
        '''
        returns the series, or config.text['no_series']
        '''
        if self.series in [None, "None"]:
            return config.text["no_series"]
        else:
            return smart_str(self.series)

    def get_edition(self):
        '''
        returns the edition or empty string
        '''
        if self.edition in [None, "None"]:
            return ""
        else:
            return smart_str(self.edition)

    def get_pretty_edition(self):
        '''
        returns the edition or config.text['no_edition']
        '''
        if self.edition in [None, "None"]:
            return config.text['no_edition']
        else:
            return smart_str(self.edition)

    def get_price(self):
        '''
        returns the price or empty string
        '''
        if self.price in [None, 'None']:
            return ""
        else:
            if self.price.isdigit():
                return "Rs. " + smart_str(self.price)
            else:
                return smart_str(self.price)

    def get_pretty_price(self):
        '''
        returns the price or config.text['no_price'] text
        '''
        if self.price in [None, "None"]:
            return config.text['no_price']
        else:
            return self.get_price()

    def get_volume(self):
        '''
        returns the volume of hte book or 1
        '''
        if self.volume in [None, 'None']:
            return 1
        else:
            return smart_str(self.volume)

    def get_gifted_by(self):
        '''
        returns the __str__() operation of gifted_by instance
        '''
        if self.gifted_by in [None, "None"]:
            return ""
        else:
            return smart_str(self.gifted_by.__str__())

    def get_pretty_gifted_by(self):
        '''
        returns __str__() operation of Gifter or helpful message
        '''
        if self.gifted_by in [None, 'None']:
            return "Not Gifted By Anyone"
        else:
            return smart_str(self.gifted_by.__str__())

    def get_title(self):
        '''
        returns the title of the book or empty string
        '''
        if self.title in [None, "None"]:
            return ''
        return smart_str(self.title)

    def get_pretty_title(self):
        '''
        same as get_title
        '''
        return self.get_title().title()

    def __str__(self):
        '''
        returns the string representation of the object
        '''
        if self.title is not None:
            return smart_str(self.get_title())
        else:
            return ""

    # What's up with all the get_* functions you ask?
    # These functions help the template system display data in a meaningful
    # way. I don't see any other use for these.

    @staticmethod
    def get_largest_accession_number():
        '''
        static method
        returns the largest accession number among all the books in Book
        '''
        return Book.objects.all().order_by("-accession_number")[0].accession_number

    def get_borrower(self):
        '''
        returns account.models.ModUser object of the person who lent this book
        or returns None
        '''
        lends = Lend.objects.filter(book=self,returned=False)
        if len(lends) == 1:
            return lends[0].user
        else:
            return None

    def get_lend_obj(self):
        '''
        returns the Lend object of the borrower of the book
        else,returns None
        '''
        lends = Lend.objects.filter(book=self,returned=False)
        if len(lends) == 1:
            return lends[0]
        else:
            return None

    def is_borrowed(self):
        '''
        checks if book is borrowed
        '''
        return self.state == 2

    def get_authors(self):
        '''
        returns a string containing all the author's of the book
        or returns empty string
        '''
        author_list = self.author.all()
        if len(author_list) > 0:
            return ", ".join([smart_str(x.get_name()) for x in author_list])
        else:
            return ""

    def get_pretty_authors(self):
        '''
        returns a string containing all the author's of the book
        or returns helpful message
        '''
        author_list = self.author.all()
        if len(author_list) > 0:
            return unicode(" र ", encoding="utf-8").join([x.get_name() for x in author_list])
        else:
            return u"No Authors"

    def get_publishers(self):
        '''
        returns string contianing publisher
        or returns empty string
        '''
        if self.publisher is not None:
            return self.publisher.__str__()
        else:
            return ""

    def get_pretty_publishers(self):
        '''
        returns string contianing publisher
        or returns helpful message
        '''
        if self.publisher is not None:
            return self.publisher.__str__()
        else:
            return "No Publishers"

    def get_catalog_publishers(self):
        '''
        returns the __catalog() operation of Publicher instance related to
        this book, else returns empty string
        '''
        if self.publisher is not None:
            return self.publisher.__catalog__()
        else:
            return ""

    def get_keywords(self):
        '''
        returns a string containing all the keywords related to this book
        else, returns empty string
        '''
        if self.keywords is not None:
            return ", ".join([smart_str(
                each.__str__()) for each in self.keywords.all() if each.__str__() not in [None, "None", ""]])
        else:
            return ""

    def get_pretty_keywords(self):
        '''
        returns a string containing all the keywords related to this book
        else, returns a helpful message
        '''
        if self.keywords is not None:
            return ", ".join([smart_str(
                each.__str__()) for each in self.keywords.all() if each.__str__() is not None])
        else:
            return "No Keywords"

    def set_borrowed_by(self, user, date=None):
        '''
        makes a person borrow this book, and changes it's state as well.
        '''
        if user.is_authenticated():
            if len([1 for x in user.groups.values() if x['name'] == 'member']) != 0:
                lend_obj = Lend.objects.create(book=self, user = user)
                if date is not None:
                    try:
                        date = [int(_) for _ in x.split('-')]
                        lend_obj.date = datetime.date(
                            date[0].split(" "),
                            date[1].split(" "),
                            date[2].split(" "))
                    except:
                        raise TypeError(
                            "value of date `{}`: does not convert into year-month-day format".format(date))
                lend_obj.save()
                self.state = 2   #is borrowed
                self.save()  #save book
            else:
                return 1
        else:
            return 1
        return 0
