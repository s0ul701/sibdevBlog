from django import forms
from captcha.fields import CaptchaField, CaptchaTextInput       # пакет формы капчи (и ее текстового поля)
from blog.models import Users, Posts
from django_summernote.widgets import SummernoteWidget      # пакет виджета текстового редактора


# TODO: убрать лишнее; возможно надо что-то изменить после тестирования; лэйблы для создания поста


class RegisterForm(forms.ModelForm):
    password_repeat = forms.CharField(min_length=6,
                                      widget=forms.PasswordInput(attrs={
                                          'placeholder': 'Repeat password',
                                          'class': 'form-control',
                                          'pattern': '[^А-Яа-яЁё]{6,}',
                                      }),
                                      )
    captcha = CaptchaField(widget=CaptchaTextInput(attrs={
                               'placeholder': 'Enter captcha',
                               'class': 'form-control',
                           }),
                           )

    class Meta:
        model = Users
        fields = ['email', 'username', 'password']
        widgets = {
            'email': forms.EmailInput(attrs={
                'placeholder': 'E-mail',
                'class': 'form-control',
            }),
            'password': forms.PasswordInput(attrs={
                'placeholder': 'Password',
                'class': 'form-control',
                'pattern': '[^А-Яа-яЁё]{6,}',
            }),
            'username': forms.TextInput(attrs={
                'placeholder': 'Login',
                'class': 'form-control',
                'pattern': '[a-zA-Z0-9_]{4,}'
            }),
        }


class AuthForm(forms.ModelForm):
    class Meta:
        model = Users
        fields = ['username', 'password']
        widgets = {
            'username': forms.TextInput(attrs={
                'placeholder': 'Username',
                'class': 'form-control',

            }),
            'password': forms.PasswordInput(attrs={
                'placeholder': 'Password',
                'class': 'form-control',

            })
        }
        help_texts = {
            'username': '',
            'password': '',
        }
        labels = {
            'username': '',
            'password': '',
        }


class PostForm(forms.ModelForm):
    field_order = {'title', 'pretext', 'text'}

    class Meta:
        model = Posts
        fields = {'title', 'pretext', 'text'}
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'Title',
                'class': 'form-control',
                'style': 'max-width: 100%;',
            }),
            'text': SummernoteWidget(attrs={
                'style': 'background: none !important',
            }),
            'pretext': SummernoteWidget(attrs={
                'style': 'background: none !important',
            }),
        }


class ProfileEditForm(forms.ModelForm):
    field_order = {'email', 'first_name', 'last_name', 'current_password', 'new_password',
                   'new_password_repeat'}

    current_password = forms.CharField(label="",
                                       widget=forms.PasswordInput(attrs={
                                           'placeholder': 'Current password',
                                           'class': 'form-control',
                                           'pattern': '[^А-Яа-яЁё]{0,}',
                                       }),
                                       required=False,
                                       )
    new_password = forms.CharField(min_length=6,
                                   label="",
                                   widget=forms.PasswordInput(attrs={
                                       'placeholder': 'New password',
                                       'class': 'form-control',
                                       'pattern': '[^А-Яа-яЁё]{6,}',
                                   }),
                                   required=False,
                                   )
    new_password_repeat = forms.CharField(min_length=6,
                                          label="",
                                          widget=forms.PasswordInput(attrs={
                                              'placeholder': 'Repeat new password',
                                              'class': 'form-control',
                                              'pattern': '[^А-Яа-яЁё]{6,}',
                                          }),
                                          required=False,
                                          )

    class Meta:
        model = Users
        fields = {'email', 'first_name', 'last_name'}
        widgets = {
            'email': forms.EmailInput(attrs={
                'placeholder': 'E-mail',
                'class': 'form-control',
            }),
            'first_name': forms.TextInput(attrs={
                'placeholder': 'First name',
                'class': 'form-control',
                'pattern': '[a-zA-Z]{2,}'
            }),
            'last_name': forms.TextInput(attrs={
                'placeholder': 'Last name',
                'class': 'form-control',
                'pattern': '[a-zA-Z]{2,}'
            }),
            'password': forms.PasswordInput(attrs={
                'placeholder': 'Current password',
                'class': 'form-control',
                'pattern': '[^А-Яа-яЁё]{6,}',
            }),
        }
