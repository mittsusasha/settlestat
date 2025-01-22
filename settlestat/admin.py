from django.contrib import admin
# Импортируем модели для их отображения в панеле админки
from .models import Settlement

# Зарегистрируем эти модели для админа
admin.site.register(Settlement)
