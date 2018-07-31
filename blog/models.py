from django.db import models
from django.contrib.auth.models import AbstractUser     # пакет для перегрузки стандартного класса User
from django_summernote.fields import SummernoteTextField

# TODO: исправить длину пароля


class Users(AbstractUser):
    username = models.CharField(null=False, blank=False, max_length=100, verbose_name="Login", unique=True)
    password = models.CharField(null=False, blank=False, max_length=500, verbose_name="Password")
    email = models.EmailField(blank=False, null=False, max_length=100, verbose_name='E-mail', unique=True)

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return self.username


class Posts(models.Model):
    title = models.CharField(null=False, blank=False, max_length=200, verbose_name="Title")
    pretext = SummernoteTextField(null=False, blank=False, max_length=500, verbose_name="Pre-text")
    text = SummernoteTextField(null=False, blank=False, verbose_name="Text")
    author = models.ForeignKey(to=Users, on_delete=models.SET_NULL, null=True, blank=False, verbose_name="Author of post")
    published_date = models.DateTimeField(auto_now_add=True, verbose_name="Published date")

    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posts"

    def __str__(self):
        return self.title
