<<<<<<< HEAD
from django.http import Http404
from django.views import View
from django.shortcuts import render
from .models import Book, Author, BookInstance, Genre
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):
    """
    Generic class-based view listing books on loan to current user.
    """
    model = BookInstance
    template_name ='catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')

class MyView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'


def index(request):
    # Генерация "количеств" некоторых главных объектов
    num_books=Book.objects.all().count()
    num_instances=BookInstance.objects.all().count()
    # Доступные книги (статус = 'a')
    num_instances_available=BookInstance.objects.filter(status__exact='a').count()
    num_authors = Author.objects.count()  # The 'all()' is implied by default.

    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1
=======
from django.shortcuts import render, get_object_or_404
from catalog.models import MyModelName, Book, Author, BookInstance, Genre  # Импортируем модели
from django.views import generic
from django.contrib.auth.models import User
#from django.contrib.auth.mixins import PermissionRequiredMixin
#from django.views.generic import ListView
#from .models import BookInstance # Импортируйте модель BookInstance

# def my_reused_view(request, my_template_name):
#     return render(request, my_template_name)
#
# def create_and_modify_record(request):
#     a_record = MyModelName(my_field_name="Instance #1")
#     a_record.save()
#     a_record.my_field_name = "New Instance Name"
#     a_record.save()
#     return render(request, 'template.html', {'record': a_record})
#
# def book_list(request):
#     all_books = Book.objects.all()
#     return render(request, 'catalog/book_list.html', {'all_books': all_books})
#
# def wild_book_list(request):
#     wild_books = Book.objects.filter(title__contains='wild')
#     number_wild_books = wild_books.count()
#     return render(request, 'catalog/wild_book_list.html', {
#         'wild_books': wild_books,
#         'number_wild_books': number_wild_books,
#     })
#
# def fiction_book_list(request):
#     books_containing_genre = Book.objects.filter(genre__name__icontains='fiction')
#     number_fiction_books = books_containing_genre.count()
#     return render(request, 'catalog/fiction_book_list.html', {
#         'books_containing_genre': books_containing_genre,
#         'number_fiction_books': number_fiction_books,
#     })

def index(request):
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    num_authors = Author.objects.count()  # The 'all()' is implied by default.

    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)  # Получаем количество посещений из сессии
    request.session['num_visits'] = num_visits + 1  # Увеличиваем количество посещений на 1 и сохраняем в сессии
>>>>>>> origin/main

    # Render the HTML template index.html with the data in the context variable.
    return render(
        request,
        'index.html',
<<<<<<< HEAD
        context={'num_books': num_books,
                 'num_instances': num_instances,
                 'num_instances_available': num_instances_available,
                 'num_authors': num_authors,
                 'num_visits': num_visits},
=======
        context={
            'num_books': num_books,
            'num_instances': num_instances,
            'num_instances_available': num_instances_available,
            'num_authors': num_authors,
            'num_visits': num_visits,  # num_visits appended
        }
>>>>>>> origin/main
    )

class BookListView(generic.ListView):
    model = Book
<<<<<<< HEAD

    paginate_by = 2

    # def get_queryset(self):
    #     return Book.objects.filter(title__icontains='war')[:5] # Получить 5 книг, содержащих 'war' в заголовке

class BookDetailView(generic.DetailView):
    model = Book

    def book_detail_view(request, pk):
        try:
            book_id = Book.objects.get(pk=pk)
        except Book.DoesNotExist:
            raise Http404("Book does not exist")

        # book_id=get_object_or_404(Book, pk=pk)

        return render(
            request,
            'catalog/book_detail.html',
            context={'book': book_id, }
        )

class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 2

class AuthorDetailView(generic.DetailView):
    model = Author

    def author_detail_view(request, pk):
        try:
            author_id = Author.objects.get(pk=pk)
        except Author.DoesNotExist:
            raise Http404("Author does not exist")

        return render(
            request,
            'catalog/author_detail.html',
            context={'author': author_id, }
        )
=======
    paginate_by = 2
    context_object_name = 'my_book_list'
    template_name = 'catalog/book_list.html'

    def get_queryset(self):
        return Book.objects.all()  # Получаем все книги

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['some_data'] = 'This is just some data'  # Добавляем дополнительные данные в контекст
        return context

class BookDetailView(generic.DetailView):
    model = Book
    template_name = 'catalog/book_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class AuthorListView(generic.ListView):
    model = Author
    template_name = 'catalog/author_list.html'  # Укажите путь к вашему шаблону
    context_object_name = 'author_list'

class AuthorDetailView(generic.DetailView):
    model = Author
    template_name = 'catalog/author_detail.html'  # Укажите путь к вашему шаблону

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['books'] = Book.objects.filter(author=self.object)  # Получаем книги данного автора
        return context

#class BorrowedBooksListView(PermissionRequiredMixin, ListView):
    model = BookInstance
    template_name = 'catalog/borrowed_books_list.html'  # Укажите путь к вашему шаблону
    context_object_name = 'borrowed_books'
    permission_required = 'catalog.can_mark_returned'  # Укажите разрешение

    def get_queryset(self):
        # Возвращает все заимствованные книги с информацией о заёмщике
        return BookInstance.objects.filter(status='o').select_related('borrower')
# # Создайте пользователя и сохраните его в базе данных
# user = User.objects.create_user('myusername', 'myemail@crazymail.com', 'mypassword')
#
# # Обновите поля и сохраните их снова
# user.first_name = 'John'
# user.last_name = 'Citizen'
# user.save()
>>>>>>> origin/main
