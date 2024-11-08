from django.contrib import admin
from .models import Author, Genre, Book, BookInstance

# Встраиваемый список книг
class BooksInline(admin.TabularInline):
    model = Book  # Указываем модель Book
    extra = 0  # Количество пустых форм для добавления новых книг

# Регистрация класса администратора для Author
@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]
    inlines = [BooksInline]  # Добавляем встроенный список книг

# Регистрация класса администратора для Genre
@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)  # Отображаем имя жанра

# Регистрация класса администратора для Book
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre')

    def display_genre(self, obj):
        """Создаёт строку для жанров."""
        return ', '.join([genre.name for genre in obj.genre.all()[:3]])

    display_genre.short_description = 'Genres'  # Название колонки в админке

# Регистрация класса администратора для BookInstance
@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_filter = ('status', 'due_back')
    list_display = ('id', 'book', 'status', 'due_back')

    fieldsets = (
        (None, {
            'fields': ('book', 'imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back')
        }),
    )