from django.urls import path
from . import views


from .views import MyView

urlpatterns = [
    path('', views.index, name='index'),
    path('books/', views.BookListView.as_view(), name='books'),
    path('book/<int:pk>/', views.BookDetailView.as_view(), name='book-detail'),
    path('author/', views.AuthorListView.as_view(), name='authors'),
    path('author/<int:pk>/', views.AuthorDetailView.as_view(), name='author-detail'),
    path('my-view/', MyView.as_view(), name='my_view'),
    path('mybooks/', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),



