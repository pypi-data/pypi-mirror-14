# -*- coding: utf-8 -*-
from django.db import models
from django.utils.encoding import smart_str, smart_text

# Create your models here.


class RestructuredText(models.Model):
    name = models.CharField(max_length=255,default="Name")
    restructuredText = models.TextField(default="")

    def __str__(self):
        return self.name

    def get_html(self):
        import markdown
        rst_dic = markdown.markdown(self.get_rst())
        return rst_dic

    def get_rst(self):
        return smart_text(self.restructuredText)

    def get_name(self):
        return smart_str(self.name)

    def set_rst(self, rest):
        '''
        args : rest

        rest - restructuredText as per python docutils restructuredText
        papameters

        creates html out of restructuredText and saves it
        '''
        self.restructuredText = rest
        self.save()
