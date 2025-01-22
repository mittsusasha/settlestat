# Нам нужно перетащить данные датасета из CSV-файла в нашу базу данных
from django.shortcuts import render
from django.http import HttpResponse
from .forms import Upload_csv_form
import pandas as pd
from settlestat.models import Settlement

# Загружаем данные из CSV файла в базу данных.


def load_csv_to_db(csv_file):       # Возможно, не лучшее решение из возможных
    # Чтение CSV файла с помощью pandas
    df = pd.read_csv(csv_file)

    # Преобразование данных и сохранение в базу данных
    for _, row in df.iterrows():
        # Создаем запись в базе данных для каждого ряда из CSV
        Settlement.objects.create(
            region=row['region'],
            municipality=row['municipality'],
            settlement=row['settlement'],
            type=row['type'],
            population=row['population'],
            children=row['children']
        )

# Функция для отображения формы загрузки CSV-файла в интерфейсе


def upload_csv(request):
    if request.method == 'POST' and request.FILES.get('csv_file'):
        form = Upload_csv_form(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file']

            # Вызываем функцию для загрузки данных из CSV в базу данных
            try:
                load_csv_to_db(csv_file)
                return render(request, 'data_loader/upload_success.html')
            except Exception as e:
                # В случае ошибки обработки файла выводим сообщение об ошибке
                return HttpResponse(f"Ошибка при обработке CSV файла: {str(e)}")

    else:
        form = Upload_csv_form()

    return render(request, 'data_loader/upload_csv.html', {'form': form})

# Функция для отображения сообщения об удачной загрузке CSV-файла


def upload_success(request):
    return render(request, 'data_loader/upload_success.html')
