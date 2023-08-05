# -*- coding: utf-8 -*-
#!/usr/bin/env python
from kantipur import kantipurToUnicode as k2u
from head.models import Book, Author, Publisher, KeyWord


def main():
    for book in Book.objects.filter(language="NP"):
#       book.title = k2u(book.title)
#       book.call_number = k2u(book.call_number)
#       for author in book.author.all():
#           uauthor = Author(name=k2u(author.name))
#           uauthor.save()
#           author.delete()
#           book.author.add(uauthor)
#       book.price = k2u(book.price)
        pub = book.publisher
        if pub is not None:
            upub = Publisher.objects.create(
                name=k2u(pub.name),
                place=k2u(pub.place),
                year=k2u(pub.year)
                )
            upub.save()
            book.publisher = upub

        for kwd in book.keywords.all():
            ukwd = KeyWord.objects.create(name=k2u(kwd.name))
            ukwd.save()
            kwd.delete()
            book.keywords.add(ukwd)
        book.save()
        print book


def replaceUnicodeNumToAscii(unicode_char):
    '''
    takes a unicode char and converts it to the ascii equililant based on the
    kantipur keyboard layput table
    '''
    out = u""
    unicode_kantipur_dict = {
        unicode(k2u(str(n))): unicode(n) for n in range(0, 10)}
    unicode_kantipur_dict.update({u"ण्": "0"})
    unicode_char.replace(u"द्ध", "4")
    for char in unicode_char:
        out += unicode_kantipur_dict.get(char, char)
    return out
