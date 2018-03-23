from __future__ import unicode_literals

from django.db import models
from datetime import datetime
import re
import bcrypt
# Create your models here.

class UserManager(models.Manager):
    def registration_validator(self,postData):
        errors = {}
        ## Registration
        if len(postData['name']) < 1:
            errors['name'] = "Name can't be empty"
        elif len(postData['name']) < 4:
            errors['name1'] = "Name must be greater than 3 characters"
        if len(postData['username']) < 1:
            errors['username'] = "Username can't be empty"
        elif len(postData['username']) < 4:
            errors['username'] = "Username must be greater than 3 characters"
        if len(postData['pw']) < 1:
            errors['pw_len'] = "Password field is empty"
        elif len(postData['pw']) < 8:
            errors['pw_len2'] = "Password is less than 8 characters"
        elif postData['pw'] != postData['confirm']:
             errors['pw'] = "Passwords do not match"
        return errors
    def login_validator(self,postData):
        errors = {}
        ## Login
        if len(postData['logPW']) < 1:
            errors['pw_len'] = "Password field is empty"
        else:
            check = User.objects.filter(username = postData['loguser'])
            if len(check) < 1:
                errors['login'] = "User does not exist"
            elif not bcrypt.checkpw(postData['logPW'].encode(), check[0].password.encode()):
                errors['password'] = "Password is incorrect"
        return errors
    def trip_validator(self,postData):
        errors = {}
        # TripAdd
        date_1 = str(postData['start'])
        date_2 = str(postData['end'])
        date_3 = str(datetime.today().strftime('%m/%d/%Y'))
        print date_1
        print date_2
        print date_3
        if len(postData['destination']) < 1:
            errors['dest'] = "Destination field is empty"
        if len(postData['description']) < 1:
            errors['desc'] = "Destcription field is empty"
        if len(postData['start']) < 1:
            errors['start'] = "Start date is empty"
        elif date_1 < date_3:
            errors['start'] = "Start date before current date"
        if len(postData['end']) < 1:
            errors['end'] = "End date is empty"
        elif date_1 > date_2:
            errors['end'] = "Start date can not be after End date"
        return errors
        

class User(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add= True)
    updated_at = models.DateTimeField(auto_now= True)
    objects = UserManager()

class Destination(models.Model):
    location = models.CharField(max_length=255)
    desc = models.CharField(max_length=255)
    start_date = models.CharField(max_length=255)
    end_date = models.CharField(max_length=255)
    creator = models.ForeignKey(User, related_name="destinations")
    joiners = models.ManyToManyField(User, related_name="joined_destinations")
    created_at = models.DateTimeField(auto_now_add= True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()