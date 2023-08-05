# -*- coding: utf-8 -*-
#!/usr/bin/python
'''
About this script

    Usage: Puts a strutured spreadhseet info into the database
            for the yalms
'''
import os
from openpyxl import load_workbook as open_workbook

from head.models import Book, Publisher, KeyWord, Author
from django.utils.encoding import smart_str
from django.utils.text import slugify
'''
A revamp is in order.
'''

def print_usage():
    print(
            '''
            SDt - Spreadsheet Database Transfer-anator
            '''
            )

## this is the struct of each column in the given spreadsheet
## the user will have to structure the file themselves

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
            '('][x]: str(x)  for x in range(0,10)
        }

SHEET = [
        'accession_number',
        'call_number',
        'author',
        'title',
        'place',
        'publisher_name',
        'year',
        'no_of_pages',
        'kw1',
        'kw2',
        'kw3',
        'kw4',
        'series',
        'edition',
        'price',
        'remarks',
        'volume',
        'language'
        ]


LANG_LIST = [
            'EN',
            'NP'
        ]

def toint(val,lang="EN"):
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


def getLang(val):
    if val == None or val == "":
        return "EN"
    else:
        if smart_str(val.upper()) in LANG_LIST:
            return smart_str(val.upper())
        else:
            raise ValueError("Language %s not found" % val)

def getVal(FILE_NAME):
    wb = open_workbook(FILE_NAME, read_only=True)
    vals=[]
    for sht in wb:
        sht_vals = []
        for row in list(sht.rows)[1:]:
            row_vals = []
            for col in list(row)[1:]:
                da = col.value
                if da.__class__ is float:
                    row_vals.append(int(da))
                else:
                    row_vals.append(da)
            sht_vals.append(row_vals)
        for each in sht_vals:
            vals.append(each)
    
    dont_have = [None] * len(vals[0])
    while dont_have in vals:
        vals.remove(dont_have)

    return vals

def main(FILE_NAME):
    values = getVal(FILE_NAME)
    vals = []
    for each in values:
        x = dict()
        while len(each) < len(SHEET):
            each.append(None)

        for array in enumerate(each):
            if array[0] == 'language':
                if array[1] == '':
                    array[1] = 'EN'
            if array[1] == "":
                x[SHEET[array[0]]] = None
            else:
                arr_0 = array[0]
                if arr_0 < len(SHEET):
                    if array[1] is not None:
                        print arr_0, array[1],FILE_NAME
                    sheet_arr = SHEET[arr_0]
                    x[sheet_arr] = smart_str(array[1])
        vals.append(x)

    for each in vals:
        if "," in each['accession_number']:
            acc_list = [_.strip(" ") for _ in each['accession_number'].split(",")]
        elif "-" in each['accession_number']:
            acc_strip = [int(_) for _ in each['accession_number'].split("-")]
            if len(acc_strip) != 2:
                raise TypeError("Range Too Many or To Few (not 2) ")
            acc_list = list(range(acc_strip[0], acc_strip[1]+1))
        else:
            acc_list = [each['accession_number']]

        for val in acc_list:
            if val.__class__ == int:
                accession_number = val
            elif val.__class__ == str:
                accession_number = val.strip(" ")
            else:
                if val.__class__ == float:
                    accession_number = int(val)
                else:
                    raise TypeError("accession number is not str or int or float")
            print each, FILE_NAME
            if accession_number == None or accession_number == "None":
                continue
            book = Book.objects.get_or_create(accession_number=toint(accession_number,each['language']),
                                    title=each['title'],
                                    no_of_pages=toint(
                                        each['no_of_pages'], each['language']))

            if book[1] is False:
                ## if the book already exists, don't create it
                continue
            else:
                book = book[0]

            if each['author'] != None:
                author = Author.objects.get_or_create(
                    name=each['author'],
                    slug = slugify(each['author']))
                if author[1]:
                    author = author[0]
                    author.save()
                else:
                    author = author[0]
                book.author.add(author)

            if (
                    each['place'] is None or
                    each['year'] is None or
                    each['publisher_name'] is None
            ) is False:
                publisher = Publisher.objects.get_or_create(
                    place=each['place'],
                    name=each['publisher_name'],
                    year=toint(each['year'],each['language']))
                if publisher[1]:
                    publisher = publisher[0]
                    publisher.save()
                else:
                    publisher = publisher[0]
                book.publisher = publisher

            if (each['call_number'] is None) is False:
                book.call_number = each['call_number']

            if (each['series'] is None) is False:
                book.series = each['series']

            if (each['edition'] is None) is False:
                book.edition = each['edition']

            if (each['price'] is None) is False:
                book.price = each['price']

            if each['volume'] != None and each['volume'] != "None":
                if each['volume'].isdigit() == True:
                    book.volume = int(each['volume'])
                else:
                    book.volume = acc_list.index(val) + 1
            else:
                book.volume = acc_list.index(val) + 1

            book.language = getLang(each['language'])

            for keyword in each['kw1'],each['kw2'],each['kw3'],each['kw4']:
                if keyword != None:
                    kw = KeyWord.objects.get_or_create(name=keyword,slug=slugify(keyword))
                    if kw[1]:
                        kw = kw[0]
                        kw.save()
                    else:
                        kw = kw[0]
                    book.keywords.add(kw)
            book.save()