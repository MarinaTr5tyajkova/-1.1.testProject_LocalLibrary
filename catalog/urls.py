from django.urls import path
from . import views
<<<<<<< HEAD

from .views import MyView

urlpatterns = [
    path('', views.index, name='index'),
    path('books/', views.BookListView.as_view(), name='books'),
    path('book/<int:pk>/', views.BookDetailView.as_view(), name='book-detail'),
    path('author/', views.AuthorListView.as_view(), name='authors'),
    path('author/<int:pk>/', views.AuthorDetailView.as_view(), name='author-detail'),
    path('my-view/', MyView.as_view(), name='my_view'),
    path('mybooks/', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),

=======

urlpatterns = [
    path('', views.index, name='index'),  # Главная страница
    path('books/', views.BookListView.as_view(), name='books'),  # Список книг
    path('book/<int:pk>/', views.BookDetailView.as_view(), name='book-detail'),  # Детальная информация о книге
    # path('url/', views.my_reused_view, {'my_template_name': 'some_path'}, name='aurl'),
    # path('anotherurl/', views.my_reused_view, {'my_template_name': 'another_path'}, name='anotherurl'),
    path('authors/', views.AuthorListView.as_view(), name='author-list'),  # Список авторов
    path('author/<int:pk>/', views.AuthorDetailView.as_view(), name='author-detail'), # детаольная информация об авторе
>>>>>>> origin/main
]