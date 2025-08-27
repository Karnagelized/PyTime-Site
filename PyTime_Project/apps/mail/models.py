
from django.db import models
from django.core.mail import send_mail
from django.template.loader import render_to_string
from PyTime_Project.settings import EMAIL_ROOT, EMAIL_CREATOR
from apps.users.models import EmailVerification



class Mail():
    """
        Базовый класс для работы с Почтой
    """

    @classmethod
    def sendMessage(cls, *, subject:str, message:str, email:str) -> bool:
        try:
            send_mail(
                subject=subject,
                message=message,
                from_email=EMAIL_ROOT,
                recipient_list=[email],
            )

            return True
        except Exception as e:
            # TODO Добавить логирование
            print(e)

        return False


    @classmethod
    def sendMessageHTML(cls, *, subject:str, email:str, messageHTML:str) -> bool:
        try:
            send_mail(
                subject=subject,
                message='Message',
                html_message=messageHTML,
                from_email=EMAIL_ROOT,
                recipient_list=[email],
            )

            return True
        except Exception as e:
            # TODO Добавить логирование
            print(e)

        return False



class VerifyEmail(Mail):
    """
        Класс для подтверждения почты через код, приходящий на почту Пользователя
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

        isSuccessSend = cls.sendMessageHTML(
            subject=cls.__getSubject(),
            email=user.email,
            messageHTML=cls.__getMessageHTML(verificationCode.code),
        )

        if not isSuccessSend:
            verificationCode.delete()

        return isSuccessSend



class SendFeedback(Mail):
    """
        Класс, для отправки обратной связи на странице контактов на почту Разработчика
    """

    @classmethod
    def __getSubject(cls, username:str) -> str:
        return f'Обратная связь: Новое сообщение от {username}'


    @classmethod
    def __getMessage(cls, text:str, email:str, username:str) -> str:
        return text + (
            '\n\n' +
            f'\nИмя отправителя: {username}' +
            f'\nПочта отправителя: {email}'
        )


    @classmethod
    def send(cls, *, email:str, username:str, text:str) -> bool:
        isSuccessSend = cls.sendMessage(
            subject=cls.__getSubject(username),
            email=EMAIL_CREATOR,
            message=cls.__getMessage(text, email, username),
        )

        return isSuccessSend
