from django import forms
from captcha.fields import CaptchaField
from blog.models import Users
import captcha


class RegisterForm(forms.ModelForm):  # TODO: переопределить поле "username"
    # field_order = ['email', 'username', 'password', 'password_repeat', 'captcha']

    password_repeat = forms.CharField(min_length=6,
                                      label="",
                                      widget=forms.PasswordInput(attrs={
                                          'placeholder': 'Repeat password',
                                          'class': 'form-control',

                                      }),

                                      )
    captcha = CaptchaField(label="", widget=captcha.fields.CaptchaTextInput(attrs={
        'placeholder': 'Enter captcha',
        'class': 'form-control',

    }),
                           )

    class Meta:
        model = Users
        fields = ['email', 'username', 'password', 'captcha']
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
