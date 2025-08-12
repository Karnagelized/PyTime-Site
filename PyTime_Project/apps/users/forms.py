
from django import forms
from django.contrib.auth.forms import (
    UserCreationForm, UserChangeForm, AdminUserCreationForm
)
from apps.users.models import CustomUser, ProfileAvatarModel
from django_bleach.forms import BleachField


# Форма для создания Пользователя в Админке
class CustomUserCreationForm(AdminUserCreationForm):

    class Meta(UserCreationForm):
        model = CustomUser
        fields =  ('username', 'email', 'first_name', 'last_name', 'aboutMe', 'avatar')


# Форма для изменения Пользователя в Админке
class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'aboutMe', 'avatar')


# Форма авторизации на сайте
class UserLoginForm(forms.ModelForm):
    email = BleachField(
        label="Почта",
        widget=forms.EmailInput(
            attrs={
                'placeholder': 'Введите почту',
                'class': 'container_form_input',
            }
        )
    )

    password = BleachField(
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


    # Валидация данных при отправке POST запроса о авторизации
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
    username = BleachField(
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

    email = BleachField(
        label='Почта',
        widget=forms.EmailInput(
            attrs={
                'placeholder': 'Введите почту',
                'class': 'container_form_input',
            }
        )
    )

    password = BleachField(
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


    # Валидации имени Пользователя
    def clean_username(self):
        username = self.cleaned_data['username']

        if CustomUser.objects.filter(username=username).exists():
            raise forms.ValidationError("Такое Имя уже существует!")

        return username


    # Валидация Email адреса Пользователя
    def clean_email(self):
        email = self.cleaned_data['email']

        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("Такой E-mail уже существует!")

        return email


# Форма для редактирования профиля Пользователя
class ProfileForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance:
            self.fields['username'].initial = user.username
            self.fields['email'].initial = user.email
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial = user.last_name
            self.fields['aboutMe'].initial = user.aboutMe

            self.fields['first_name'].required = False
            self.fields['last_name'].required = False
            self.fields['aboutMe'].required = False


    username = BleachField(
        max_length=150,
        label='Имя пользователя',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Введите имя',
                'class': 'container_form_input w-100',
                'readonly': 'readonly',
            }
        )
    )

    email = BleachField(
        label='Почта',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Введите почту',
                'class': 'container_form_input w-100',
                'readonly': 'readonly',
            }
        )
    )

    first_name = BleachField(
        max_length=100,
        min_length=5,
        label='Имя',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Введите имя',
                'class': 'container_form_input w-100',
            }
        )
    )

    last_name = BleachField(
        max_length=100,
        min_length=5,
        label='Фамилия',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Введите фамилию',
                'class': 'container_form_input w-100',
            }
        )
    )

    aboutMe = BleachField(
        max_length=255,
        min_length=1,
        label='Обо мне',
        widget=forms.Textarea(
            attrs={
                'placeholder': 'Расскажите о себе',
                'class': 'container_form_input form_textarea w-100',
            }
        )
    )


    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'aboutMe')


class AvatarProfileForm(forms.ModelForm):
    avatar = forms.FileField(
        label='',
        widget=forms.FileInput(
            attrs={
                'class': 'input_file_button',
            }
        )
    )

    class Meta:
        model = ProfileAvatarModel
        fields = ('avatar',)
