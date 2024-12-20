from django.contrib import admin
from .models import Author, Genre, Book, BookInstance, Language

# Register your models here.

#admin.site.register(Book)
#admin.site.register(Author)
admin.site.register(Genre)
#admin.site.register(BookInstance)
admin.site.register(Language)

class BooksInline(admin.TabularInline):
    model = Book

# Определите класс администратора
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]

    inlines = [BooksInline]

admin.site.register(Author, AuthorAdmin)

# Для отображения экземпляров книг (BookInstance) в виде встроенной таблицы на странице редактирования книги (Book).
class BooksInstanceInline(admin.TabularInline):
    model = BookInstance
# Отвечает за администрирование модели Book. Он определяет, как будут отображаться записи книг в административной панели
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre')
    inlines = [BooksInstanceInline]

# Управляет моделью BookInstance, которая представляет собой конкретные экземпляры книги (например, конкретные физические копии)
@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('book', 'status', 'borrower', 'due_back', 'id')
    list_filter = ('status', 'due_back')

    fieldsets = (
        (None, {
            'fields': ('book','imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back','borrower')
        }),
    )


