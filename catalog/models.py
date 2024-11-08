from django.db import models
from django.urls import reverse
import uuid  # Импортируем модуль uuid


class MyModelName(models.Model):
    """Типичный класс модели, производный от класса Model."""
    my_field_name = models.CharField(max_length=20, help_text='Введите описание поля')

    class Meta:
        ordering = ['-my_field_name']

    def get_absolute_url(self):
        """Возвращает URL-адрес для доступа к определенному экземпляру MyModelName."""
        return reverse('model-detail-view', args=[str(self.id)])

    def __str__(self):
        """Строка для представления объекта MyModelName."""
        return self.my_field_name

class Author(models.Model):
    """Модель для представления автора."""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)

    def get_absolute_url(self):
        """Возвращает URL-адрес для доступа к экземпляру автора."""
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        """Строка для представления объекта автора."""
        return '%s, %s' % (self.last_name, self.first_name)

    class Meta:
        ordering = ['last_name']  # Сортировка по фамилии

class Genre(models.Model):
    """Модель для представления жанра книги."""
    name = models.CharField(max_length=200)

    def __str__(self):
        """Строка для представления объекта жанра."""
        return self.name

class Book(models.Model):
    """Модель для представления книги."""
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True)
    summary = models.TextField(max_length=1000)
    isbn = models.CharField('ISBN', max_length=13)
    genre = models.ManyToManyField(Genre)

    def __str__(self):
        """Строка для представления объекта книги."""
        return self.title

class BookInstance(models.Model):
    """Модель для представления конкретного экземпляра книги."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    book = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)

    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    status = models.CharField(max_length=1, choices=LOAN_STATUS, blank=True, default='m')

    class Meta:
        ordering = ["due_back"]

    def __str__(self):
        """Строка для представления экземпляра книги."""
        return '%s (%s)' % (self.id, self.book.title)

