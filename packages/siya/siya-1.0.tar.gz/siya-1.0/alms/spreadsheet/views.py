# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.utils.encoding import smart_str,smart_text
from StringIO import StringIO
from django.core.files import File
from django.http import HttpResponse

from openpyxl import Workbook
# Create your views here.
from head.models import Book, Author, Publisher, Lend

import datetime

def returnSpreadSheet(queryset, filename, title):
    '''
    This takes a queryset and returns a spreadsheet
    the queryset objects must have a Object.get_all_attr_for_spreadsheet() 
    function
    '''
    wb = Workbook(write_only=True)
    ws = wb.create_sheet()
    all_attr = title
    ws.append(all_attr)
    for object_ in queryset: 
        attrs = [smart_str(_[1]) for _ in object_.get_all_attr_for_spreadsheet()]
        ws.append(attrs)
    wb.save(filename)
    response = HttpResponse(open(filename,"r").read(),content_type="application/spreadsheet")
    response['Content-Disposition'] = 'attachment; filename='+filename
    return response


def getBorrowedBookData(request):
    borrowed_books_lend_obj = Lend.objects.filter(returned__gt = False)
    all_attr = [_[0] for _ in borrowed_books_lend_obj[0].get_all_attr_for_spreadsheet()]
    return returnSpreadSheet(queryset=borrowed_books_lend_obj,filename="BorrowedBooks.xls", title=all_attr)


def getAllBookData(request):
    all_books = Book.objects.order_by("accession_number")
    all_attr = [_[0] for _ in all_books[0].get_all_attr_for_spreadsheet()]
    return returnSpreadSheet(queryset=all_books,filename="AllBooks.xls", title=all_attr)

def getAllAuthorData(request):
    all_authors = Author.objects.order_by("name")
    all_attr = [_[0] for _ in all_authors[0].get_all_attr_for_spreadsheet()]
    return returnSpreadSheet(queryset=all_authors,filename="AllAuthors.xls", title=all_attr)

def getAllPublisherData(request):
    all_publishers = Publisher.objects.order_by("name")
    all_attr = [_[0] for _ in all_publishers[0].get_all_attr_for_spreadsheet()]
    return returnSpreadSheet(queryset=all_publishers,filename="AllPublishers.xls", title=all_attr)

def getBooksWithoutCallNumber(request):
    books = Book.objects.filter(call_number="")
    if len(books) > 0:
        all_attr = [_[0] for _ in books[0].get_all_attr_for_spreadsheet()]
    else:
        return HttpResponse("No Such Books Found")
    return returnSpreadSheet(queryset=books,filename="BooksWithoutCallNumber.xls", title=all_attr)

