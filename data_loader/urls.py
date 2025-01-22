from django.urls import path
from .views import FileLoader, FileRemover, UploadSuccess     # Импортируем наш класс


# Подключаем маршруты для функционала нашего приложения
urlpatterns = [
    path('upload/', FileLoader.as_view(),
         name='upload_csv'),  # Загрузка CSV
    path('success/', UploadSuccess.as_view(),
         name='upload_success'),  # Сообщение об успешной загрузке
    path('delete/', FileRemover.as_view(),
         name='delete_csv'),  # Удаление CSV
]
