from django import forms
from captcha.fields import CaptchaField
from blog.models import Users
import captcha


class RegisterForm(forms.ModelForm):  # TODO: переопределить поле "username"
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
        fields = ['email', 'username', 'password', 'password_repeat', 'captcha']
        widgets = {
            'email': forms.EmailInput(attrs={
                'placeholder': 'E-mail',
                'class': 'form-control',

            }),
            'username': forms.TextInput(attrs={
                'placeholder': 'Username',
                'class': 'form-control',

            }),
            'password': forms.PasswordInput(attrs={
                'placeholder': 'Password',
                'class': 'form-control',

            }),
        }

    field_order = ['email', 'username', 'password', 'password_repeat', 'captcha']


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
                'placeholder': 'Repeat password',
                'class': 'form-control',

            })
        }
