from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class Users(AbstractUser):
    username = models.CharField(null=False, blank=False, help_text="Enter login", max_length=100, verbose_name="Login", unique=True)
    password = models.CharField(null=False, blank=False, help_text="Enter password", max_length=100, verbose_name="Password")

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return self.username


class Posts(models.Model):
    title = models.CharField(null=False, blank=False, help_text="Enter title of post", max_length=100, verbose_name="Title")
    text = models.TextField(null=False, blank=False, help_text="Enter text of post", verbose_name="Text")
    author = models.ForeignKey(to=Users, on_delete=models.SET_NULL, null=True, blank=False, help_text="Enter author of post", verbose_name="Author of post")
    published_date = models.DateTimeField(auto_now_add=True, verbose_name="Published date")

    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posts"

    def __str__(self):
        return self.title
