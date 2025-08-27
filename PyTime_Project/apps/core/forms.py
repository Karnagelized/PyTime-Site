
from django.forms import Form
from django.forms.widgets import Textarea, EmailInput, TextInput
from django.http import HttpRequest
from django_bleach.forms import BleachField
from apps.users.models import CustomUser



class ContactFeedbackForm(Form):
    """
        Форма обратной связи на странице контактов
    """

    def __init__(self, user:CustomUser=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if user is not None:
            if user.is_authenticated:
                self.fields['email'].initial = user.email


    email = BleachField(
        label='Email',
        widget=EmailInput(
            attrs={
                'class': 'container_form_input w-100',
                'placeholder': 'Введите Email'
            }
        )
    )

    name = BleachField(
        label='Имя',
        widget=TextInput(
            attrs={
                'class': 'container_form_input w-100',
                'placeholder': 'Введите Имя'
            }
        )
    )

    message = BleachField(
        label='Сообщение',
        widget=Textarea(
            attrs={
                'class': 'feedback_input w-100',
                'placeholder': 'Введите сообщение для обратной связи',
            }
        )
    )
