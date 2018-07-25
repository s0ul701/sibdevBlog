from django import forms
from captcha.fields import CaptchaField, CaptchaTextInput  # пакетаформы капчи (и ее текстового поля)
from blog.models import Users

# TODO: убрать лишнее


class RegisterForm(forms.ModelForm):
    password_repeat = forms.CharField(min_length=6,
                                      label="",
                                      widget=forms.PasswordInput(attrs={
                                          'placeholder': 'Repeat password',
                                          'class': 'form-control',
                                      }),

                                      )
    captcha = CaptchaField(label="",
                           widget=CaptchaTextInput(attrs={
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
        help_texts = {
            'email': '',
            'password': '',
            'password_repeat': '',
            'captcha': '',
            'username': 'Allowed symbol: A-Z, a-z, 0-9, _',
        }
        labels = {
            'email': '',
            'password': '',
            'password_repeat': '',
            'captcha': '',
            'username': '',
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
