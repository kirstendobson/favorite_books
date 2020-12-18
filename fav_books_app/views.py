from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Count
import bcrypt
from .models import *

def index(request):
    return render(request, 'index.html')

## Login and Register
def register(request):
    if request.method=='POST':
        errors=User.objects.validator(request.POST)
        if len(errors):
            for key, value in errors.items():
                messages.error(request, value)
                return redirect('/')
        else:
            password = request.POST['pword']
            pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
            print(pw_hash)
            new_user = User.objects.create(
                f_name=request.POST['f_name'],
                l_name=request.POST['l_name'],
                email=request.POST['email'],
                pword=pw_hash
            )
            request.session['user_id']=new_user.id
            request.session['user_name']=f"{new_user.f_name} {new_user.l_name}"
            return redirect('/books')
    return redirect('/')

def login(request):
    if request.method=='POST':
        errors=User.objects.login_validator(request.POST)
        if len(errors):
            for key, value in errors.items():
                messages.error(request, value)
                return redirect('/')
        logged_user = User.objects.filter(email=request.POST['login_email'])
        if logged_user:
            logged_user=logged_user[0]
            if bcrypt.checkpw(request.POST['login_pword'].encode(), logged_user.pword.encode()):
                request.session['user_id']=logged_user.id
                request.session['user_name']=f"{logged_user.f_name} {logged_user.l_name}"
                return redirect('/books')
            return redirect('/')
        return redirect ('/')
    return redirect('/')

def logout(request):
    request.session.clear()
    return redirect('/')

## Favorite Books
def books(request):
    if 'user_id' not in request.session:
        return redirect('/')
    context={
        "all_books": Book.objects.all().order_by('created_at'),
        "current_user": User.objects.get(id=request.session['user_id'])
    }
    return render(request, 'main_page.html', context)

def add_book(request):
    if request.method=='POST':
        errors = Book.objects.validator(request.POST)
        if len(errors):
            for key, value in errors.items():
                messages.error(request, value)
                return redirect('/')
        else:
            new_book = Book.objects.create(
                title=request.POST['title'],
                desc=request.POST['desc'],
                uploaded_by=User.objects.get(id=request.session['user_id'])
            )
            this_user = User.objects.get(id=request.session['user_id'])
            this_user.liked_books.add(new_book)
            return redirect('/books')
    return redirect('/')

def view_book(request, book_id):
    context = {
        "book": Book.objects.get(id=book_id),
        "current_user": User.objects.get(id=request.session['user_id'])
    }
    return render(request, 'one_book.html', context)

def update_book(request, book_id):
    book_to_update = Book.objects.get(id=book_id)
    book_to_update.title = request.POST['title']
    book_to_update.desc = request.POST['desc']
    book_to_update.save()
    return redirect('/books')

def delete_book(request, book_id):
    book_to_delete = Book.objects.get(id=book_id)
    book_to_delete.delete()
    return redirect('/books')

def favorite(request, book_id):
    book_to_favorite = Book.objects.get(id=book_id)
    user = User.objects.get(id=request.session['user_id'])
    user.liked_books.add(book_to_favorite)
    return redirect('/books')

def unfavorite(request, book_id):
    book_to_unfavorite = Book.objects.get(id=book_id)
    user = User.objects.get(id=request.session['user_id'])
    user.liked_books.remove(book_to_unfavorite)
    return redirect('/books')

def view_user(request, user_id):
    context = {
        "user": User.objects.get(id=user_id)
    }
    return render(request, 'user.html', context)