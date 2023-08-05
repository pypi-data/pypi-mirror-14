# -*- coding: utf-8 -*-
from django.db import models
from django.utils.encoding import smart_str


# Create your models here.

# Concept of a generic field :
#    Book --|---->0-- GenericField --|---->0-- GenericFieldValue
#
# Description :
#    A generic field can have many books. Each generic field can also have
#    many values that corelate to a certain book.
#
#                                GenericField
#                                    |
#                                    |
#                                    |
#                ----------------------------------------
#               |                                        |
#               |                                        |
#               |                                        |
#        Generic Field Link                             Name
#               |
#               |
#               |
#        ----------------
#       |                |
#       |                |
#       |                |
#     Value             Book
#
#
#                fig : Tree for misc fields of books
#
# Generic fields are only indirectly related to a book (through Generic Field
# Links). A generic field contains a name ( such as "Author", "Title" and a
# link to Generic Field Link. The generic field link in turn contains a value
# such as "1", "Mahabharat" and the link to a book.


class GenericFieldLink(models.Model):
    '''
    this model stores the value in GenericField for each book
    '''
    value = models.TextField(null=True)
    book = models.ForeignKey('head.Book')

    def get_value(self):
        return smart_str(self.value)

    def get_book(self):
        return self.book

    def get_book_id(self):
        return self.book.id

    @staticmethod
    def try_get(cls, book):
        '''
        Liek Class.objects.get operation, except it doesnt throw error

        When more than one objects with such book is found, the first object
        in the stack is returned. If no objects are found, an empty string is
        returned.
        '''
        objects = cls.objects.filter(book=book)
        n_objs = objects.count()
        if n_objs == 0:
            return ""
        elif n_objs > 1:
            return objects[0]
        else:
            # there is 1 object
            return objects[0]

    def __str__(self):
        return "value  for %s book" % self.book.get_title()


class GenericField(models.Model):
    '''
    this is a generic field for a book
    this can be anything you want it to be

    this has two attrs :
    key - name of the field
    value - value that is stored for each book in the db
    '''
    key = models.CharField(max_length=255, default="What is My name?")
    value = models.ManyToManyField(GenericFieldLink)
    date_added = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.key

    def get_key(self):
        '''return the key'''
        return smart_str(self.key)

    def _get_value_obj(self, book_id):
        '''return the GenericFieldBookLink object for that book'''
        book = Book.objects.get(id=book_id)
        return self.value.get(book=book)

    def get_value(self, book_id):
        '''
        returns the value as unicode string
        '''
        return self._get_value_obj(book_id=book_id).get_value()

    def set_value(self, value, book):
        x = GenericFieldLink.objects.create(book=book, value=value)
        self.value.add(x)

    def get_programatic_key(self):
        '''
        return the key as something without spaces or other invalid chars
        '''
        return self.get_key().replace(" ", "_")
