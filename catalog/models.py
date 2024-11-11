from django.db import models
from django.urls import reverse  # Используется для генерации URL-адресов путем изменения шаблонов URL-адресов
import uuid  # Требуется для уникальных экземпляров книг
from django.contrib.auth.models import User
from datetime import date


class Genre(models.Model):
    """
    Модель, представляющая книжный жанр (например, научную фантастику, нон-фикшн).
    """
    name = models.CharField(max_length=200, help_text="Enter a book genre (e.g. Science Fiction, French Poetry etc.)")

    def __str__(self):
        """
        Строка для представления объекта модели (на сайте администратора и т.д.)
        """
        return self.name


class Book(models.Model):
    """
    Модель, представляющая книгу (но не конкретную копию книги).
    """
    title = models.CharField(max_length=200)
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    summary = models.TextField(max_length=1000, help_text="Enter a brief description of the book")
    isbn = models.CharField('ISBN', max_length=13,
                            help_text='13 Charact <a href="https://www.isbn-international.org/content/what-isbn">ISBN номер</a>')
    genre = models.ManyToManyField('Genre', help_text="Select a genre for this book")

    def __str__(self):
        """
        Строка для представления модельного объекта.
        """
        return self.title

    def get_absolute_url(self):
        """
        Возвращает URL-адрес для доступа к определенному экземпляру книги.
        """
        return reverse('book-detail', args=[str(self.id)])

    def display_genre(self):
        """
        Создает строку для жанра. Это необходимо для отображения жанра в Admin.
        """
        return ', '.join([genre.name for genre in self.genre.all()[:3]])

    display_genre.short_description = 'Genre'


class BookInstance(models.Model):
    """
    Модель, представляющая конкретный экземпляр книги (т.е. ту, которую можно взять напрокат в библиотеке).
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          help_text="Unique ID for this particular book across whole library")
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    status = models.CharField(max_length=1, choices=LOAN_STATUS, blank=True, default='m', help_text='Book availability')

    class Meta:
        ordering = ["due_back"]
        permissions = (("can_mark_returned", "Set book as returned"),)

    def __str__(self):
        """
        Строка для представления модельного объекта
        """
        return f'{self.id} ({self.book.title})'

    def book_title(self):
        return str(self.book.title)

    def due_back_format(self):
        return '.'.join((str(self.due_back)).split('-'))

    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False


class Author(models.Model):
    """
    Модель, представляющая автора.
    """
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)

    def get_absolute_url(self):
        """
        Возвращает URL-адрес для доступа к конкретному экземпляру author.
        """
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        """
        Строка для представления модельного объекта.
        """
        return f'{self.last_name} {self.first_name}'

    def life_period(self):
        return '.'.join((str(self.date_of_birth)).split('-')) + (
            ' - ' + '.'.join((str(self.date_of_death)).split('-')) if self.date_of_death else '')

class Language(models.Model):
    name = models.CharField(max_length=200)