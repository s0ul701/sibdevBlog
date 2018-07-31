from django.contrib import admin
from blog.models import Users, Posts
from django_summernote.admin import SummernoteModelAdmin    # пакет модели текстового редактора


class UserAdmin(admin.ModelAdmin):
    fields = ('username', 'password', 'email', 'first_name', 'last_name', 'is_active')      # отображение полей на странице редактирования (+ их порядок)
    list_display = ('username', 'password', 'email', 'first_name', 'last_name', 'is_active')     # отображение полей в таблице модели (+ их порядок)


admin.site.register(Users, UserAdmin)


class PostAdmin(SummernoteModelAdmin):
    fields = ('author', 'title', 'pretext', 'text')
    list_display = ('title', 'author', 'published_date')
    # summernote_fields = ('pretext', 'text')       # поля, отображающиеся с помощью текстового редактора


admin.site.register(Posts, PostAdmin)
