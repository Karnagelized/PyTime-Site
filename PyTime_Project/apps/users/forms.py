
from django import forms
from django.contrib.auth.forms import (
    UserCreationForm, UserChangeForm, AdminUserCreationForm
)
from apps.users.models import CustomUser, ProfileAvatarModel
from django_bleach.forms import BleachField
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV3



class CustomUserCreationForm(AdminUserCreationForm):
    """
        Форма для создания Пользователя в Админке
    """


    class Meta(UserCreationForm):
        model = CustomUser
        fields =  ('username', 'email', 'first_name', 'last_name', 'aboutMe', 'avatar')



class CustomUserChangeForm(UserChangeForm):
    """
        Форма для изменения Пользователя в Админке
    """


    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'aboutMe', 'avatar')



class UserLoginForm(forms.Form):
    """
        Форма авторизации
    """

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


    def clean_email(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        user = CustomUser.objects.filter(email=email).first()

        if not CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError(
                'Такого Email не существует.'
            )

        return email


    def clean_password(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if not email or not password:
            return

        user = CustomUser.objects.filter(email=email).first()

        if not user or not user.check_password(password):
            raise forms.ValidationError(
                'Неверный пароль.'
            )

        return password



class UserVerifyEmail(forms.Form):
    """
        Форма подтверждения почты через код
    """

    code = BleachField(
        min_length=6,
        max_length=6,
        label='',
        widget=forms.TextInput(
            attrs={
                'class': 'container_form_input verify-code-input w-100 text-center',
                'maxlength': '6',
                'pattern': '[0-9]{6}',
                'inputmode': 'numeric',
                'autocomplete': 'off',
                'placeholder': 'Введите 6-ти значный код',
            }
        )
    )


    def clean_code(self):
        code = self.cleaned_data['code']

        # Проверяем что только цифры
        if not code.isdigit():
            raise forms.ValidationError(
                'Код должен содержать только цифры'
            )

        # Проверяем длину
        if len(code) != 6:
            raise forms.ValidationError(
                'Код должен содержать ровно 6 цифр'
            )

        return code



class UserRegistrationForm(forms.ModelForm):
    """
        Форма регистрации
    """

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

    captcha = ReCaptchaField(
        label='',
        widget=ReCaptchaV3()
    )


    class Meta:
        model = CustomUser
        fields = ('email', 'password',)


    def clean_email(self):
        email = self.cleaned_data['email']

        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("Такой E-mail уже существует!")

        return email



class ProfileForm(forms.ModelForm):
    """
        Форма редактирования профиля Пользователя
    """

    def __init__(self, user:'CustomUser'=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if user is not None:
            self.instance = user

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


    def clean_username(self):
        username = self.cleaned_data['username']
        userFind = CustomUser.objects.filter(username=username).first()

        if self.data.get('email') != userFind.email:
            raise forms.ValidationError(
                'Такое Имя Пользователя уже занято!'
            )

        return username


class AvatarProfileForm(forms.ModelForm):
    """
        Форма редактирования аватара Пользователя на странице профиля
    """

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
