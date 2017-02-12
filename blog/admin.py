from django.contrib import admin
from blog.models import Posts, Categories, Comment
# from tinymce.widgets import TinyMCE
from django.db import models
from ckeditor.widgets import CKEditorWidget
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class PostsAdmin(admin.ModelAdmin):
    icon = '<i class="material-icons">bubble_chart</i>'
    exclude = ['posted']
    prepopulated_fields = {'slug': ('title',)}
    list_display = ['title', 'author', 'created_on', 'date', 'time', 'published']
    formfield_overrides = {
        models.TextField: {'widget': CKEditorUploadingWidget},
    }

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        obj.save()


class CategoriesAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ['title']


# Register your models here.
admin.site.register(Posts, PostsAdmin)
admin.site.register(Categories, CategoriesAdmin)
admin.site.register(Comment)
