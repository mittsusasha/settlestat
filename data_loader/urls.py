from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_csv, name='upload_csv.html'),  # Загрузка CSV
    # path('success/', views.upload_success, name='upload_success'),  # Не пригодится, переход на эту страницу будет из представления upload_csv
]
