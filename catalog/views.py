from django.shortcuts import render
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import permission_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
import datetime
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .forms import RenewBookForm
from .models import Book, Author, BookInstance, Genre



# Функция для отображения домашней страницы сайта

def index(request):
    # Генерация "количеств" некоторых главных объектов
    num_books=Book.objects.all().count()
    num_instances=BookInstance.objects.all().count()

    # Доступные книги (статус = 'a')
    num_instances_available=BookInstance.objects.filter(status__exact='a').count()
    num_authors = Author.objects.count()  # метод ALL() применен по умолчанию.

    # Количество посещений этой страницы, учитываемое в переменной сессии.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    # Отображаем HTML-шаблон index.html с данными в контексте.
    return render(
        request,
        'index.html',
        context={'num_books': num_books,
                 'num_instances': num_instances,
                 'num_instances_available': num_instances_available,
                 'num_authors': num_authors,
                 'num_visits': num_visits},
    )


# Этот класс наследуется от generic.ListView, что позволяет создавать представления для отображения списков объектов.
class BookListView(generic.ListView):
    model = Book
    paginate_by = 2

    def get_queryset(self):
        return Book.objects.order_by('author')

# Предоставить подробную информацию об одном экземпляре книги из базы данных
class BookDetailView(generic.DetailView):
    model = Book

# Способ организовать отображение списка объектов модели в Django с поддержкой разбиения на страницы
class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 10

# Для отображения подробной информации об одном экземпляре модели 'Author'
class AuthorDetailView(generic.DetailView):
    model = Author

# Отвечает за отображение списка книг, взятых напрокат конкретным пользователем
class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):
    model = BookInstance
    template_name ='catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')

# Для отображения списка всех книг, находящихся на руках у пользователей
class AllLoanedBooksListView(PermissionRequiredMixin, generic.ListView):
    permission_required = 'catalog.can_mark_returned'
    model = BookInstance
    template_name = 'catalog/all_borrowed.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')



'''Эта функция обеспечивает библиотекарям возможность продлевать срок возврата книг. 
Она включает проверку прав доступа, обработку форм и взаимодействие с базой данных,'''

@permission_required('catalog.can_mark_returned')
def renew_book_librarian(request, pk):

    book_inst = get_object_or_404(BookInstance, pk=pk)

    # Если это POST - запрос, то обработайте данные формы
    if request.method == 'POST':

        # Создание экземпляра формы и заполнение его данными из запроса (привязка):
        form = RenewBookForm(request.POST)

        # Проверка, действительна ли форма:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            book_inst.due_back = form.cleaned_data['renewal_date']
            book_inst.save()

            # Перенаправление на новый URL:
            return HttpResponseRedirect(reverse('all-borrowed') )

    # Если это GET (или любой другой метод), создать форму по умолчанию.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date,})

    return render(request, 'catalog/book_renew_librarian.html', {'form': form, 'bookinst':book_inst})






class AuthorCreate(PermissionRequiredMixin, CreateView):
    permission_required = 'catalog.can_mark_returned'
    model = Author
    fields = '__all__'
    # initial={'date_of_death':'12/10/2016',}

class AuthorUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = 'catalog.can_mark_returned'
    model = Author
    fields = ['first_name','last_name','date_of_birth','date_of_death']

class AuthorDelete(PermissionRequiredMixin, DeleteView):
    permission_required = 'catalog.can_mark_returned'
    model = Author
    success_url = reverse_lazy('authors')

class BookCreate(PermissionRequiredMixin, CreateView):
    permission_required = 'catalog.can_mark_returned'
    model = Book
    fields = '__all__'

class BookUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = 'catalog.can_mark_returned'
    model = Book
    fields = '__all__'

class BookDelete(PermissionRequiredMixin, DeleteView):
    permission_required = 'catalog.can_mark_returned'
    model = Book
    success_url = reverse_lazy('books')







