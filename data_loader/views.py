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
    # Переменная для вывода сообщения об успешной загрузке... можно было сделать лучше, кажется
    success_message = None

    if request.method == 'POST' and request.FILES.get('csv_file'):
        form = Upload_csv_form(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file']

            # Вызываем функцию для загрузки данных из CSV в базу данных
            try:
                load_csv_to_db(csv_file)
                # Записываем сообщение об успехе
                success_message = "Ваш датасет успешно загружен в базу данных приложения!"
            except Exception as e:
                # В случае ошибки обработки файла выводим сообщение об ошибке
                return HttpResponse(f"Ошибка при обработке CSV файла: {str(e)}")

        else:
            # Если форма вообще не является валидной
            return HttpResponse("Ошибка: Неправильный файл!")

    else:
        form = Upload_csv_form()

        return render(request, 'data_loader/upload_csv.html', {
            'form': form,
            'success_message': success_message,  # Передаем сообщение об успехе
        })

# Функция для отображения сообщения об удачной загрузке CSV-файла


def upload_success(request):
    return render(request, 'data_loader/upload_success.html')

# Функция для удаления данных датасета из таблицы


def delete_csv(request):
    if request.method == 'POST':
        # Проверим, действительно ли пользователь хочет удалить данные
        # Если приходит запрос POST, подтверждаем удаление
        try:
            # Удаляем все записи из таблицы Settlement
            Settlement.objects.all().delete()
            return render(request, 'data_loader/delete_confirm.html', {
                'message': 'Данные датасета успешно удалены из базы данных.',
                'return_url': 'upload_csv'  # Ссылка на меню загрузки
            })
        except Exception as e:
            return render(request, 'data_loader/delete_confirm.html', {
                'message': f'При удалении данных возникла ошибка: {str(e)}',
                'return_url': 'upload_csv'  # Ссылка на меню загрузки
            })

    # Если запрос GET, показываем страницу с подтверждением
    return render(request, 'data_loader/delete_confirm.html', {
        # 'message': 'Вы уверены, что хотите удалить датасет из базы данных приложения? После удаления вам придётся загружать CSV-файл с датасетом заново. Пожалуйста, подтвердите своё решение.',
        'return_url': 'upload_csv'  # Ссылка на меню загрузки
    })
