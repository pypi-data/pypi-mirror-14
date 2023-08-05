# -*- coding: utf-8 -*-
'''


 _____                 _   _                       _                  _ _ 
| ____|_ __ ___  _ __ | |_(_)_ __   ___  ___ ___  (_)___    _____   _(_) |
|  _| | '_ ` _ \| '_ \| __| | '_ \ / _ \/ __/ __| | / __|  / _ \ \ / / | |
| |___| | | | | | |_) | |_| | | | |  __/\__ \__ \ | \__ \ |  __/\ V /| | |
|_____|_| |_| |_| .__/ \__|_|_| |_|\___||___/___/ |_|___/  \___| \_/ |_|_|
                |_|                                                       



If you can make one heap of all your winnings
    And risk it on one turn of pitch-and-toss,
And lose, and start again at your beginnings
    And never breathe a word about your loss;
If you can force your heart and nerve and sinew
    To serve your turn long after they are gone,   
And so hold on when there is nothing in you
    Except the Will which says to them: 'Hold on!'

If you can talk with crowds and keep your virtue,   
    Or walk with Kings-nor lose the common touch,
If neither foes nor loving friends can hurt you,
    If all men count with you, but none too much;
If you can fill the unforgiving minute
    With sixty seconds' worth of distance run,   
Yours is the Earth and everything that's in it,   
    And-which is more-you'll be a Man, my son!

'''

from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.models import BaseUserManager, Group
from django.db import models
from django.utils import timezone
from django.core.mail import EmailMessage
from django.core.urlresolvers import reverse


import datetime

# Create your models here.

class UserType(models.Model):
    '''
    This class describes the type of user
    The types of users are: 
        * member
        * volunteer
        * managers
    '''
    _type = models.CharField(max_length=20)
    slug = models.SlugField()

    def type(self):
        return self._type

    def __str__(self):
        return self._type


class UserManager(BaseUserManager):

    def create(self,
            username,
            super_user=False,
            first_name=None,
            last_name=None,
            password=None, 
            **extra_fields):
        '''
            Dont grant this user staff access!!
            There is a seperate file to grant user superuser status
        '''

        if not username:
            raise ValueError("Username is required to create User")

        user = self.model(username=username,
                first_name=first_name,
                last_name=last_name,
                **extra_fields
                )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password):
        '''
        like create, but also makes the user a saff, andn gives them superuser access
        '''
        if not username:
            raise ValueError("username is required")
        if not password:
            raise ValueError("Password is required")

        user = self.create(username=username, password=password,super_user=True)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

    def add(self, user):
	'''
	  add new user
	'''
        self.viewers.add(user.viewer)


class ModUser(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=90,null=True,blank=True)
    last_name = models.CharField(max_length=90,null=True,blank=True)
    username = models.CharField(max_length=25, unique=True,blank=True)

    date_joined = models.DateTimeField('Date Joined',default=timezone.now)

    sex = models.CharField(max_length=6,
            null=True,
            choices=(
                ('male','male'),
                ('female','female'),
                ))

    addr_ward_no = models.CharField(max_length=20, null=True,blank=True)
    addr_tole = models.CharField(max_length=100, null=True,blank=True)
    addr_municipality = models.CharField(max_length=100, null=True,blank=True)

    telephone_home = models.IntegerField(null=True,blank=True)
    telephone_mobile = models.IntegerField(null=True,blank=True)

    parent_name = models.CharField(max_length=255,null=True,blank=True)
    parent_telephone_number = models.IntegerField(null=True,blank=True)

    school_name = models.CharField(max_length=255,null=True,blank=True)
    school_telephone = models.IntegerField(null=True,blank=True)
    school_class = models.CharField(max_length=5,null=True,blank=True)
    school_roll_no = models.CharField(max_length=3,null=True,blank=True)
    school_varified = models.NullBooleanField(default=False)
    
    date_of_birth = models.DateField(null=True,blank=True)

    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "username"

    def get_address(self):
        return u"{0} ward, {1}, {2}".format(self.addr_ward_no, self.addr_tole, self.addr_municipality)

    def get_telephone(self):
        return u"home: {0}, mobile: {1}, parent's: {2}".format(self.telephone_home, self.telephone_mobile, self.parent_telephone_number)
    
    def get_age(self):
        if self.date_of_birth in [None,"None"]:
            return ""
        return datetime.date.today().year - self.date_of_birth.year

    
    def save(self,commit=True,create_new=False, *args, **kwargs):
        if not self.is_active:
            self.send_email_activation_confirmation()
        if commit:
            super(ModUser, self).save(*args,**kwargs)

    def is_male(self):
        return self.sex == "male"
    
    def is_female(self):
        return self.sex == "female"
            
    def get_short_name(self):
        if self.first_name is None:
            return self.username
        else:
            return self.first_name

    def get_name(self):
        if self.first_name is None or self.last_name is None:
            return self.username
        return u"{0} {1}".format(self.first_name, self.last_name).title()



    def get_all_attr(self):
        return [
            ('Name', self.get_name()),
            ("Username", self.username),
            ("Gender", self.sex),
            ("Age", self.get_age()),
            ("Parent's Name", self.parent_name),
            ("Phone Number", self.get_telephone()),
            ("School Name", self.school_name),
            ("Class", self.school_class),
            ("Roll No.", self.school_roll_no),
            ("School Phone Number", self.school_telephone),
        ]

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.get_name()
