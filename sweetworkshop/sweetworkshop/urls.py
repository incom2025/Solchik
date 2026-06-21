"""sweetworkshop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
]
# Використовуйте include(), щоб додавати URL з каталогу програми
from django.urls import include
from django.urls import path
urlpatterns += [
    path('catalog/', include('catalog.urls')),
]
# Додати URL співвідношення, щоб перенаправити запити з кореневого URL, на URL програми
from django.views.generic import RedirectView
urlpatterns += [
    path('', RedirectView.as_view(url='/catalog/', permanent=True)),
]
# Використовуйте static(), щоб додати співвідношення для статичних файлів
# Лише на період розробки
from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
from django.conf.urls import include
# Додаємо URL-адреси автентифікації сайту Django (для входу, виходу з системи, керування паролями)
urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
]

from django.conf import settings  # new
from django.urls import path, include  # new
from django.conf.urls.static import static  # new

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("imagess.urls")), # new
]

if settings.DEBUG:  # new
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
