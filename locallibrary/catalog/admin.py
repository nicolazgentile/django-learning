from django.contrib import admin
from .models import Book, Author, Genre, BookInstance, Language, Publisher, Employee, Category


# Register your models here.
class BookInstanceInline(admin.TabularInline):
    model = BookInstance
    extra = 0
# admin.site.register(Book)
# Register the Admin classes for Book using the decorator
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre')
    inlines = [BookInstanceInline]

class BookInline(admin.TabularInline):
    model = Book
    extra = 1
# admin.site.register(Author)
# Define the admin class
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]
    inlines = [BookInline]
# Register the admin class with the associated model
admin.site.register(Author, AuthorAdmin)

@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    list_display = ('name', 'country', 'website')
    inlines = [BookInline]

    fieldsets = (
        (None, {
            'fields': ('name', 'website')
        }),
        ('Location', {
            'fields': ('city', 'state_province', 'country')
        }),
    )


admin.site.register(Genre)


# admin.site.register(BookInstance)
# Register the Admin classes for BookInstance using the decorator
@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('book', 'due_date', 'due_back', 'get_return_days', )
    list_filter = ('status', 'due_back', )

    fieldsets = (
        (None, {
            'fields': ('book', 'imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back')
        }),
    )


admin.site.register(Language)


class EmployeeInline(admin.TabularInline):
    model = Employee
    extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    # list_display = ('name', 'country', 'website')
    inlines = [EmployeeInline]


admin.site.register(Employee)
