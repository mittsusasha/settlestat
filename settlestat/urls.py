"""
URL configuration for settlestat project.

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
from . import views
from data_loader import views as dl_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.Settlements_first_view.as_view()),
    # Подключаем также маршруты приложения data_loader
    # path('upload/', include('data_loader.urls')),
    path('upload/', include('data_loader.urls')),  # Загрузка CSV
    # path('success/', include('data_loader.urls')),  # Не пригодится, переход на эту страницу будет из представления upload_csv
    path('success/', include('data_loader.urls')),
    path('delete/', include('data_loader.urls')),
    # Подключаем маршруты для функционала нашего приложения статистики
    path('statistics_tools/', include('statistics_tools.urls')),
]
