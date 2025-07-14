
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AdminUserCreationForm
from django.core.exceptions import ValidationError
from django.forms import TextInput

from core.models import CustomUser, Comment


# Форма для создания Пользователя в Админке
class CustomUserCreationForm(AdminUserCreationForm):

    class Meta(UserCreationForm):
        model = CustomUser
        fields =  ('username', 'email')

# Форма для изменения Пользователя в Админке
class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('username', 'email')


# Форма авторизации на сайте
class UserLoginForm(forms.ModelForm):
    email = forms.EmailField(
        label="Почта",
        widget=forms.EmailInput(
            attrs={
                'placeholder': 'Введите почту',
                'class': 'container_form_input',
            }
        )
    )
    password = forms.CharField(
        max_length=50,
        min_length=5,
        label='Пароль',
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Введите пароль',
                'class': 'container_form_input',
            }
        )
    )


    class Meta:
        model = CustomUser
        fields = ('email', 'password')

    def clean(self):
        cleaned_data = super().clean()
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if email and password:
            user = CustomUser.objects.filter(email=email).first()

            if not user or not user.check_password(password):
                raise forms.ValidationError('Неверный пароль или email!')

        return cleaned_data


# Форма регистрации на сайте
class UserRegistrationForm(forms.ModelForm):
    username = forms.CharField(
        max_length=50,
        min_length=5,
        label='Имя пользователя',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Введите имя пользователя',
                'class': 'container_form_input',
            }
        )
    )
    email = forms.EmailField(
        label='Почта',
        widget=forms.EmailInput(
            attrs={
                'placeholder': 'Введите почту',
                'class': 'container_form_input',
            }
        )
    )
    password = forms.CharField(
        max_length=50,
        min_length=5,
        label='Пароль',
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Введите пароль',
                'class': 'container_form_input',
            }
        )
    )

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password',)


    def clean_username(self):
        username = self.cleaned_data['username']

        if CustomUser.objects.filter(username=username).exists():
            raise forms.ValidationError("Такое Имя уже существует!")

        return username


    def clean_email(self):
        email = self.cleaned_data['email']

        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("Такой E-mail уже существует!")

        return email