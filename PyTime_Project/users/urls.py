
from django.urls import path
from users.views import (
    UserProfileView, LoginUserView, LogoutUserView, RegistrationUserView,
    passwordResetEnterMail, passwordResetEnterCode, passwordResetEnterNewPassword
)
from PyTime_Project.settings import DEBUG


# Маршруты приложения "users"
urlpatterns = [
    path('profile', UserProfileView.as_view(), name='profilePage'),
    path('login', LoginUserView.as_view(), name='loginUser'),
    path('logout', LogoutUserView.as_view(), name='logoutUser'),
    path('registration', RegistrationUserView.as_view(), name='registrationUser'),
]

if DEBUG:
    urlpatterns += [
        path('password-reset', passwordResetEnterMail, name='passwordResetEnterMail'),
        path('password-reset-enter-code', passwordResetEnterCode, name='passwordResetEnterCode'),
        path('password-reset-enter-password', passwordResetEnterNewPassword, name='passwordResetEnterNewPassword'),
    ]
