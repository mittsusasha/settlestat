from django.urls import path
from .views import FileToDatabase, FileLoader, FileRemover   # Импортируем наш класс


# Подключаем маршруты для функционала нашего приложения
urlpatterns = [
    path('upload/', FileLoader.as_view(),
         name='upload_csv'),  # Загрузка CSV
    path('success/', FileToDatabase.as_view(),  # Без этого выдаёт AttributeError
         name='upload_success'),  # Сообщение об успехе загрузки
    path('delete/', FileRemover.as_view(),
         name='delete_csv'),  # Удаление CSV
]
