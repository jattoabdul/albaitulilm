from django.contrib import admin
from bookstore.models import *
from django.db import models
from ckeditor_uploader.widgets import CKEditorUploadingWidget


# Register your models here.
class CategoriesAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ['title']


class PublisherAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']
    list_display = ['name', 'address', 'country', 'website']


class AuthorAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('first_name',)}
    search_fields = ['first_name', 'last_name', 'nationality']
    list_display = ['first_name', 'last_name', 'nationality', 'email']
    formfield_overrides = {
            models.TextField: {'widget': CKEditorUploadingWidget},
        }


class LanguageAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']


class BookAdmin(admin.ModelAdmin):
    # icon = '<i class="material-icons">bubble_chart</i>'
    exclude = ['posted']
    prepopulated_fields = {'slug': ('title',)}
    list_display = ['title', 'publisher', 'language', 'category', 'isbn',
                    'publication_year', 'uploaded_by', 'download_no']
    formfield_overrides = {
        models.TextField: {'widget': CKEditorUploadingWidget},
    }

    def save_model(self, request, obj, form, change):
        obj.uploaded_by = request.user
        obj.save()


# Register your models here.
admin.site.register(Categories, CategoriesAdmin)
admin.site.register(Publisher, PublisherAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Language, LanguageAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(Review)
