# -*- coding: utf-8 -*-
from difflib import SequenceMatcher

from django.utils.encoding import smart_str


def search(needle, heystack):
    needle = smart_str(needle.lower().strip(" "))
    heystack = smart_str(heystack.lower().strip(" "))
    if len(needle) == 0:
        return heystack
    needlel = needle.split(" ") ## get a list of all the words in the needle
    ranks = []
    heystackl = heystack.split(" ")
    if len(needlel) == 1:
        for each in heystackl:
            if needle in each:
                ranks.append(1 - 1./(len(heystack) - heystack.index(each)))
            else:
                seq = SequenceMatcher(None, needle, each)
                ranks.append(round(seq.ratio(), 3))
        return max(ranks) ## return the highest rank
    else:
        for _ in range(0,len(needlel)): ranks.append([])
        
        for needeach in needlel:
            for heyeach in heystackl:
                if needeach in heyeach:
                    ranks[needlel.index(needeach)].append(
                            1 - 1./max(len(heystack) - heystack.index(heyeach),1))
                else:
                    seq = SequenceMatcher(None, needeach, heyeach)
                    ranks[needlel.index(needeach)].append(seq.ratio())
        rank_out = []
        for each in ranks:
            if each.__class__ == float:
                rank_out.append(each)
            else:
                rank_out.append(max(each))
        return sum(rank_out) / len(rank_out)

    return None


def searchGenericField(searchstr, genericField):
    books = []
    genLinkQuerySet = genericField.value.all()

    for genLink in genLinkQuerySet:
        rank = search(searchstr, genLink.value)
        if rank > 0.6:
            books.append((genLink.book, rank))
    books = sorted(books, key=lambda book: book[1], reverse=True)
    books = [book[0] for book in books]
    return books


def searchBookAuthor(searchstr, bookQuerySet):
    books = []
    for book in bookQuerySet:
        rank = search(searchstr, book.get_authors())
        if rank > 0.6:
            books.append((book, rank))
    books = sorted(books, key=lambda book: book[1], reverse=True)
    books = [book[0] for book in books]
    return books


def searchBookTitle(searchstr, bookQuerySet):
    books = []
    for book in bookQuerySet:
        rank = search(searchstr, book.get_title())
        if rank > 0.6:
            books.append((book, rank))
    books = sorted(books, key=lambda book:book[1],reverse=True)
    books = [book[0] for book in books]
    return books


def searchBookKeywords(searchstr, bookQuerySet):
    books = []
    ranks = []
    for book in bookQuerySet:
        rank = search(searchstr, book.get_keywords())
        if rank > 0.6:
            books.append((book, rank))
        ranks.append(rank)
    books = sorted(books, key=lambda book:book[1],reverse=True)
    books = [book[0] for book in books]
    if max(ranks) < 0.85:
        return searchBookTitle(searchstr, bookQuerySet) + searchBookAuthor(searchstr, bookQuerySet)
    else:
        return books
