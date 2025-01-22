from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_csv, name='upload_csv.html'),  # Загрузка CSV
    path('success/', views.upload_success, name='upload_success'),  # Сообщение об успехе загрузки 
    path('delete/', views.delete_csv, name='delete_csv'),  # Удаление CSV
]
