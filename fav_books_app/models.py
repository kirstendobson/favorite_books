from django.db import models
import re, bcrypt

class UserManager(models.Manager):
    def validator(self, postData):
        email_check=re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        errors={}
        if len(postData['f_name']) < 2:
            errors['f_name'] = "First Name must be at least 2 characters"
        if len(postData['l_name']) < 2:
            errors['l_name'] = "First Name must be at least 2 characters"
        if not email_check.match(postData['email']):
            errors['email'] = "Email must be a valid email address"
        if postData['pword'] != postData['cnfrm_pword']:
            errors['pword_match'] = "Password and Confirm Password must match"
        if len(postData['pword']) < 8:
            errors['pword'] = "Password must be at least 8 characters"
        check = User.objects.filter(email=postData['email'])
        if check:
            errors['emails'] = "Email already registered"
        return errors
    def login_validator(self, postData):
        errors={}
        check = User.objects.filter(email=postData['login_email'])
        if not check:
            errors['login_email'] = "Email has not been registered"
        else:
            if not bcrypt.checkpw(postData['login_pword'].encode(), check[0].pword.encode()):
                errors['login_email'] = "Email and password do not match"
        return errors

class User(models.Model):
    f_name = models.CharField(max_length=25)
    l_name = models.CharField(max_length=25)
    email = models.CharField(max_length=45)
    pword = models.CharField(max_length=25)
    #liked_books = list of books a given user likes 
    #books_uploaded = list of books uploaded by a given user
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class BookManager(models.Manager):
    def validator(self, postData):
        errors={}
        if len(postData['title']) < 1:
            errors['title'] = "You must provide a title"
        if len(postData['desc']) < 5:
            errors['desc'] = "Description must be at least 5 characters"
        return errors

class Book(models.Model):
    title = models.CharField(max_length=255)
    desc = models.CharField(max_length=255)
    uploaded_by = models.ForeignKey(User, related_name="books_uploaded", on_delete=models.CASCADE)
    users_who_like = models.ManyToManyField(User, related_name="liked_books")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = BookManager()