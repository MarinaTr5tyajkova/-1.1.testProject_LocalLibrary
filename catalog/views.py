from django.shortcuts import render
from catalog.models import MyModelName  # Импортируем модель
from .models import Book  # Импортируем модель Book

def create_and_modify_record(request):
    # Создание новой записи
    a_record = MyModelName(my_field_name="Instance #1")
    a_record.save()  # Сохранение объекта в базе данных

    # Доступ к полям и изменение их
    print(a_record.id)  # Выводит ID новой записи
    print(a_record.my_field_name)  # Выводит 'Instance #1'

    # Изменение значения поля
    a_record.my_field_name = "New Instance Name"
    a_record.save()  # Сохранение изменений

    return render(request, 'template.html', {'record': a_record})  # Пример возврата записи в шаблон


def book_list(request):
    # Получаем все записи модели Book
    all_books = Book.objects.all()

    # Передаем все книги в контекст шаблона
    return render(request, 'catalog/book_list.html', {'all_books': all_books})


def wild_book_list(request):
    # Получаем все книги, содержащие 'wild' в заголовке
    wild_books = Book.objects.filter(title__contains='wild')

    # Подсчитываем количество таких книг
    number_wild_books = wild_books.count()

    # Передаем отфильтрованные книги и их количество в контекст шаблона
    return render(request, 'catalog/wild_book_list.html', {
        'wild_books': wild_books,
        'number_wild_books': number_wild_books,
    })


def fiction_book_list(request):
    # Получаем все книги, жанр которых содержит 'fiction'
    books_containing_genre = Book.objects.filter(genre__name__icontains='fiction')

    # Подсчитываем количество таких книг
    number_fiction_books = books_containing_genre.count()

    # Передаем отфильтрованные книги и их количество в контекст шаблона
    return render(request, 'catalog/fiction_book_list.html', {
        'books_containing_genre': books_containing_genre,
        'number_fiction_books': number_fiction_books,
    })


