
from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import reverse, redirect


class LoginRequiredMixin(AccessMixin):
    """
        Миксин, требующий авторизацию пользователя
    """

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(reverse('loginUser'))

        return super().dispatch(request, *args, **kwargs)


# def login_required_mixin_decorator(view):
#     """
#         Декоратор на основе миксина LoginRequiredMixin
#     """
#     mixin = LoginRequiredMixin()
#
#     def wrapper(self, request, *args, **kwargs):
#         response = mixin.dispatch(request, *args, **kwargs)
#
#         return view(self, request, *args, **kwargs)
#
#     return wrapper
