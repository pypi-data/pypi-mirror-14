# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Book, KeyWord, Author, Publisher

class BookAdmin(admin.ModelAdmin):
    search_fields = ["author__name","keywords__name", "title","call_number",'accession_number']

class GenericAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


# Register your models here.

admin.site.register(Book, BookAdmin)
admin.site.register(Author, GenericAdmin)
admin.site.register(KeyWord, GenericAdmin)
admin.site.register(Publisher)
