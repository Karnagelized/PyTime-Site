
from django.urls import path
from core.views import mainPage

# Маршруты приложения "core"
urlpatterns = [
    path('', mainPage)
]
