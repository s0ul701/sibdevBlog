from django.contrib import admin
from blog.models import Users, Posts

# Register your models here.


class UserAdmin(admin.ModelAdmin):      # TODO: настроить поля редактирования модели
    # fields = ("login", "password")      # отображение полей на странице редактирования
    list_display = ("username", "password", "email", "first_name", "last_name", "is_active", )     # отображение полей в таблице модели


admin.site.register(Users, UserAdmin)


class PostAdmin(admin.ModelAdmin):
    fields = ("title", "author", "text")
    list_display = ("title", "author", "text", "published_date")


admin.site.register(Posts, PostAdmin)
