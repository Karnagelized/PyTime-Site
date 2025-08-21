
from django.db import models
from django.core.mail import send_mail
from django.template.loader import render_to_string
from PyTime_Project.settings import EMAIL_ROOT
from apps.users.models import EmailVerification


class VerifyEmail():
    """
        Класс для отправки ссылки с кодом подтверждения
    """

    @classmethod
    def __getSubject(cls) -> str:
        return 'Безопасность PyTime: Подтверждение email'


    @classmethod
    def __getMessageHTML(cls, code:str) -> str:
        return render_to_string(
            'email_message.html',
            context={
                'verificationCode': code,
            }
        )


    @classmethod
    def send(cls, *, user:'CustomUser') -> bool:
        verificationCode = EmailVerification.create(
            user=user,
        )

        try:
            send_mail(
                subject=cls.__getSubject(),
                message='Message',
                html_message=cls.__getMessageHTML(verificationCode.code),
                from_email=EMAIL_ROOT,
                recipient_list=[user.email],
            )

            return True
        except Exception as e:
            # TODO Добавить логирование
            verificationCode.delete()

            print(e)

        return False
