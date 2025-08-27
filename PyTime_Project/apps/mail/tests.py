
from unittest.mock import patch, MagicMock
from django.template.loader import render_to_string
from django.test import TestCase
from apps.mail.models import Mail, VerifyEmail, SendFeedback
from django.core.mail import send_mail
from PyTime_Project.settings import EMAIL_ROOT, EMAIL_CREATOR
from apps.users.factories import UserCustomFactory
from apps.users.models import EmailVerification



class TestMailClassTestCase(TestCase):
    """
        Тестирование базового класса работы с Почтой
    """

    @patch('apps.mail.models.send_mail')
    def test_valid_send_message(self, mock_send_mail:MagicMock):
        """
            Тестирование удачной попытки отправки сообщения на почту
        """

        mock_send_mail.return_value = 1

        mailData = {
            'subject': 'TestSubject',
            'message': 'TestMessage',
            'email': 'testAny@mail.ru',
        }

        isSuccess = Mail.sendMessage(
            **mailData,
        )

        self.assertTrue(isSuccess)
        mock_send_mail.assert_called_once_with(
            subject=mailData['subject'],
            message=mailData['message'],
            from_email=EMAIL_ROOT,
            recipient_list=[mailData['email']],
        )


    @patch('apps.mail.models.send_mail')
    def test_invalid_send_message(self, mock_send_mail:MagicMock):
        """
            Тестирование неудачной попытки отправки сообщения на почту
        """

        mock_send_mail.side_effect = Exception('SMTP error for testing Mail class')

        mailData = {
            'subject': 'TestSubject',
            'message': 'TestMessage',
            'email': 'testAny@mail.ru',
        }

        isSuccess = Mail.sendMessage(
            **mailData,
        )

        self.assertFalse(isSuccess)
        mock_send_mail.assert_called_once_with(
            subject=mailData['subject'],
            message=mailData['message'],
            from_email=EMAIL_ROOT,
            recipient_list=[mailData['email']],
        )


    @patch('apps.mail.models.send_mail')
    def test_valid_send_message_html(self, mock_send_mail:MagicMock):
        """
            Тестирование удачной попытки отправки сообщения с HTML на почту
        """

        mock_send_mail.return_value = 1

        mailData = {
            'subject': 'TestSubject',
            'email': 'testAny@mail.ru',
            'messageHTML': render_to_string('email_message.html'),
        }

        isSuccess = Mail.sendMessageHTML(
            **mailData,
        )

        self.assertTrue(isSuccess)
        mock_send_mail.assert_called_once_with(
            subject=mailData['subject'],
            html_message=mailData['messageHTML'],
            message='Message',
            from_email=EMAIL_ROOT,
            recipient_list=[mailData['email']],
        )


    @patch('apps.mail.models.send_mail')
    def test_invalid_send_message_html(self, mock_send_mail:MagicMock):
        """
            Тестирование неудачной попытки отправки сообщения с HTML на почту
        """

        mock_send_mail.side_effect = Exception('SMTP error for testing Mail class')

        mailData = {
            'subject': 'TestSubject',
            'email': 'testAny@mail.ru',
            'messageHTML': render_to_string('email_message.html'),
        }

        isSuccess = Mail.sendMessageHTML(
            **mailData,
        )

        self.assertFalse(isSuccess)
        mock_send_mail.assert_called_once_with(
            subject=mailData['subject'],
            html_message=mailData['messageHTML'],
            message='Message',
            from_email=EMAIL_ROOT,
            recipient_list=[mailData['email']],
        )



class TestVerifyEmailClassTestCase(TestCase):
    """
        Тестирование класса для отправки кода подтверждения на почту Пользователя
    """

    @patch('apps.mail.models.send_mail')
    def test_valid_send_message_html(self, mock_send_mail:MagicMock):
        """
            Тестирование удачной попытки отправки HTML сообщения с кодом на почту
        """

        mock_send_mail.return_value = 1

        user = UserCustomFactory(
            email='testemail@mail.ru',
        )

        isSuccess = VerifyEmail.send(
            user=user,
        )

        verificationCode = EmailVerification.objects.filter(user=user).first()

        self.assertTrue(isSuccess)
        mock_send_mail.assert_called_once_with(
            subject='Безопасность PyTime: Подтверждение email',
            html_message=render_to_string(
                'email_message.html',
                context={
                    'verificationCode': verificationCode.code,
                }
            ),
            message='Message',
            from_email=EMAIL_ROOT,
            recipient_list=[user.email],
        )


    @patch('apps.mail.models.send_mail')
    def test_invalid_send_message_html(self, mock_send_mail:MagicMock):
        """
            Тестирование неудачной попытки отправки HTML сообщения с кодом на почту
        """

        mock_send_mail.side_effect = Exception('SMTP error for testing VerifyEmail class')

        user = UserCustomFactory(
            email='testemail@mail.ru',
        )

        isSuccess = VerifyEmail.send(
            user=user,
        )

        self.assertFalse(isSuccess)



class TestSendFeedbackClassTestCase(TestCase):
    """
        Тестирование класса для отправки обратной связи на почту Пользователя
    """

    @patch('apps.mail.models.send_mail')
    def test_valid_send_feedback_message(self, mock_send_mail:MagicMock):
        """
            Тестирование удачной попытки отправки сообщения обратной связи на почту сайта
        """

        mock_send_mail.return_value = 1

        user = UserCustomFactory(
            username='TestUsername',
            email='testemail@mail.ru',
        )

        mailData = {
            'subject': f'Обратная связь: Новое сообщение от {user.username}',
            'message': 'Hello world!',
        }

        isSuccess = SendFeedback.send(
            email=user.email,
            username=user.username,
            text=mailData['message'],
        )

        sendMessage = mailData['message'] + (
            '\n\n' +
            f'\nИмя отправителя: {user.username}' +
            f'\nПочта отправителя: {user.email}'
        )

        self.assertTrue(isSuccess)
        mock_send_mail.assert_called_once_with(
            subject=mailData['subject'],
            message=sendMessage,
            from_email=EMAIL_ROOT,
            recipient_list=[EMAIL_CREATOR],
        )


    @patch('apps.mail.models.send_mail')
    def test_invalid_send_feedback_message(self, mock_send_mail:MagicMock):
        """
            Тестирование неудачной попытки отправки сообщения обратной связи на почту сайта
        """

        mock_send_mail.side_effect = Exception('SMTP error for testing VerifyEmail class')

        user = UserCustomFactory(
            username='TestUsername',
            email='testemail@mail.ru',
        )

        mailData = {
            'subject': f'Обратная связь: Новое сообщение от {user.username}',
            'message': 'Hello world!',
        }

        isSuccess = SendFeedback.send(
            email=user.email,
            username=user.username,
            text=mailData['message'],
        )

        self.assertFalse(isSuccess)
