# -*- coding: utf-8 -*-
from django.db import models

import datetime


from django.conf import settings
import os
import codecs

from miscFields.models import GenericField


import hashlib


def md5Checksum(filePath):
    with open(filePath, 'rb') as fh:
        m = hashlib.md5()
        while True:
            data = fh.read(8192)
            if not data:
                break
            m.update(data)
        return m.hexdigest()


GET_MAIN_COLOR = "SELECT main_color FROM org_configs"
GET_ACCENT_COLOR = "SELECT accent_color FROM org_configs"

CONFIG_INI = os.path.join(settings.BASE_DIR, "config.ini")
CONFIG_SQLITE = os.path.join(settings.BASE_DIR, "config.sqlite")
TEXT_INI = os.path.join(settings.BASE_DIR, "text.ini.np")


class Globals:
    '''
    this is a wrapper arpund the configs.models.Organization class
    to support the Globals class data structure.
    '''
    def __init__(self):
        import configparser
        self.config = configparser.ConfigParser()
        self.text_config = configparser.ConfigParser()
        self.config.read(CONFIG_INI)
        self.text_config.read(TEXT_INI)
        self.set_vals()
        self.checksum = ""
        self.load()
        self.db_load()

    def set_vals(self):
        self.books = self.config['books']
        self.books_columns = self.config['columns']
        self.yalms = self.config['alms']
        self.misc = self.config['misc']
        self.text = self.text_config['text']
        self.db_load()

    def db_load(self):
        import sqlite3
        config_db = sqlite3.connect(CONFIG_SQLITE)
        self.main_color = config_db.cursor().execute(GET_MAIN_COLOR).fetchone()[0]
        self.accent_color = config_db.cursor().execute(GET_ACCENT_COLOR).fetchone()[0]

    def load(self):
        import configparser
        self.config = configparser.ConfigParser()
        self.text_config = configparser.ConfigParser()
        self.config.read(CONFIG_INI)
        self.text_config.read(TEXT_INI)

    def reload(self):
        if self.file_is_same() is False:
            self.load()
        self.db_load()

    def refresh(self):
        self.load()
        self.reload()

    def file_is_same(self):
        checksum = md5Checksum(CONFIG_INI)
        if checksum != self.checksum:
            self.checksum = checksum
            return False
        return True

    def add(self, section, key, value):
        self.config.set(section, key, value)
        self.save()
        self.load()

    def save(self):
        with codecs.open(CONFIG_INI, "w", encoding="utf-8") as configfile:
            self.config.write(configfile)


class AccessionNumberCount(models.Model):
    accession_number = models.IntegerField(default=0)

    @staticmethod
    def add1():
        acc_nos = AccessionNumberCount.objects.all()
        if len(acc_nos) == 1:
            acc_nos[0].accession_number += 1
            acc_nos[0].save()
            return 0
        else:
            return 1

    @staticmethod
    def get_no():
        acc_nos = AccessionNumberCount.objects.all()
        if len(acc_nos) == 1:
            return acc_nos[0].accession_number
        else:
            return 0


config = Globals()


TYPES = [
    config.text['title'],
    config.text['author'],
    config.text['accession_number'],
    config.text['call_number'],
    config.text['publisher'],
    config.text['keyword']
    ]


def get_ip_addr():
    import socket
    return socket.gethostbyname(socket.gethostname())


def addGlobalContext(context=None):
    types = TYPES + ["."+_.get_key() for _ in GenericField.objects.all()]
    print types
    global_dict = {
        "globals": Globals(),  # user Globals() not config because the updates
        # to config files need to be seen immediately
        # * config is a cached object fo Globals class *
        "date": datetime.date.today(),
        'main_color': "#"+str(config.main_color),
        'accent_color': "#"+str(config.accent_color),
        'types': types,
        'ip_addr': get_ip_addr()
        }
    if context is not None and context.__class__ == dict:
        context.update(global_dict)
        return context
    elif context is None:
        return global_dict
    else:
        raise TypeError("context is not a dictionary")


def no_to_en(value):
    '''
    convert number to nepali
    '''
    nepali_numbers = [
        u'\u0966',
        u'\u0967',
        u'\u0968',
        u'\u0969',
        u'\u096a',
        u'\u096b',
        u'\u096c',
        u'\u096d',
        u'\u096e',
        u'\u096f',
        ]
    out = ""
    for _ in value:
        if _ in nepali_numbers:
            out += unicode(nepali_numbers.index(_))
        else:
            out += _
    return out


def no_to_np(value):
    '''
    convert number to nepali
    '''
    config = Globals()
    out = ""
    value = unicode(value)
    if unicode(value).isdigit() is True:
        for _ in value:
            np_txt = config.text.get(_, None)
            if np_txt is None:
                out += _
            else:
                out += np_txt
    return out


