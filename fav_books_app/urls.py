from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('create_user', views.register),
    path('login', views.login),
    path('books', views.books),
    path('logout', views.logout),
    path('create_book', views.add_book),
    path('books/<int:book_id>', views.view_book),
    path('books/<int:book_id>/update', views.update_book),
    path('books/<int:book_id>/delete', views.delete_book),
    path('books/<int:book_id>/unfavorite', views.unfavorite),
    path('books/<int:book_id>/favorite', views.favorite),
    path('user/<int:user_id>', views.view_user)
]