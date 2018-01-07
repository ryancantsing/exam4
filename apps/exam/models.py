from __future__ import unicode_literals
import re
import bcrypt
from django.db import models
from datetime import datetime

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
NAME_REGEX = re.compile(r'^[A-Za-z]\w+$')

class UserManager(models.Manager):
    def validate_login(self, post_data):
        errors = []
        # check DB for post_data['email']
        if len(self.filter(email=post_data['email'])) > 0:
            # check this user's password
            user = self.filter(email=post_data['email'])[0]
            if not bcrypt.checkpw(post_data['password'].encode(), user.password.encode()):
                errors.append('email/password incorrect')
        else:
            errors.append('email/password incorrect')

        if errors:
            return errors
        return user

    def validate_registration(self, post_data):
        errors = []
        if len(post_data['name']) < 2 or len(post_data['username']) < 2:
            errors.append("name fields must be at least 3 characters")
        if len(post_data['password']) < 8:
            errors.append("password must be at least 8 characters")
        if not re.match(NAME_REGEX, post_data['name']) or not re.match(NAME_REGEX, post_data['username']):
            errors.append('name fields must be letter characters only')
        if not re.match(EMAIL_REGEX, post_data['email']):
            errors.append("invalid email")
        if len(Users.objects.filter(email=post_data['email'])) > 0:
            errors.append("email already in use")
        if post_data['password'] != post_data['password_confirm']:
            errors.append("passwords do not match")

        if not errors:
            # make our new user
            # hash password
            hashed = bcrypt.hashpw((post_data['password'].encode()), bcrypt.gensalt(5))

            new_user = self.create(
                name=post_data['name'],
                username=post_data['username'],
                email=post_data['email'],
                password=hashed
            )
            return new_user
        return errors

class ItemManager(models.Manager):
    def validate_item(self, post_data, user):
        errors = []
        if len(post_data['name']) < 3:
            errors.append("Name of Item must be at least 3 characters!")
        if len(Items.objects.filter(name=post_data['name'])) > 0:
            errors.append("Item has already been added!")
        if not errors:
            new_item = self.create(
                name=post_data['name'],
                added_by = user,
            )
            return new_item
        return errors



class Users(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    date_of_birth = models.DateField(null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    def __str__(self):
        return self.email

class Items(models.Model):
    name = models.CharField(max_length=255)
    added_by = models.ForeignKey(Users, related_name="user_uploaded", null=True)
    wished_at = models.ManyToManyField(Users, related_name="wished_items")
    created_at = models.DateTimeField(auto_now_add = True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = ItemManager()
    def __str__(self):
        return self.name
