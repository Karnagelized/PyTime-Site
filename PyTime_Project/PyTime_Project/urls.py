"""
URL configuration for PyTime_Project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from core.views import (
    badRequest, forbidden,
    pageNotFound, internalServerError
)
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('admin', admin.site.urls),
    path('', include('core.urls')),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


handler400 = badRequest
handler403 = forbidden
handler404 = pageNotFound
handler500 = internalServerError
