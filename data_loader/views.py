# Нам нужно перетащить данные датасета из CSV-файла в нашу базу данных
from django.views import View   # Чтобы наследовать от этого базового класса наш класс
from django.shortcuts import render
from django.http import HttpResponse
from .forms import Upload_csv_form
import pandas as pd
from settlestat.models import Settlement


# Этот класс используется для загрузки файлов (пока что только в формате CSV)
class FileToDatabase(View):

    # Метод для загрузки данных из CSV файла в базу данных приложения
    def csv_to_db(self, csv_file):       # Возможно, не лучшее решение из возможных
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

    # Метод для отображения сообщения об удачной загрузке CSV-файла
    def get(self, request):
        return render(request, 'data_loader/upload_success.html')


# Этот класс отображает форму загрузки
class FileLoader(View):

    # Метод для отображения данных о загрузке CSV-файла
    def post(self, request):
        form = Upload_csv_form(request.POST, request.FILES)
        if form.is_valid() and request.FILES.get('csv_file'):
            csv_file = request.FILES['csv_file']
            # Вызываем функцию для загрузки данных из CSV в базу данных
            try:
                loader = FileToDatabase()
                loader.csv_to_db(csv_file)
                # Записываем сообщение об успехе
                success_message = "Ваш датасет успешно загружен в базу данных приложения!"
                return render(request, 'data_loader/upload_csv.html', {
                    'form': form,
                    'success_message': success_message,  # Передаем сообщение об успехе
                })
            except Exception as e:
                # В случае ошибки обработки файла выводим сообщение об ошибке
                return HttpResponse(f"Ошибка при обработке CSV файла: {str(e)}")
            # Если форма вообще не является валидной
        return HttpResponse("Ошибка: Неправильный файл!")

    # Метод для отображения формы загрузки CSV-файла в интерфейсе
    def get(self, request):
        form = Upload_csv_form()
        return render(request, 'data_loader/upload_csv.html', {
            'form': form,
            'success_message': None,
        })


# Этот класс используется для удаления датасета из таблицы базы данных приложения
class FileRemover(View):

    # Проверим, действительно ли пользователь хочет удалить данные
    # Если приходит запрос POST, подтверждаем удаление
    def post(self, request):
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
    def get(self, request):
        return render(request, 'data_loader/delete_confirm.html', {
            # 'message': 'Вы уверены, что хотите удалить датасет из базы данных приложения? После удаления вам придётся загружать CSV-файл с датасетом заново. Пожалуйста, подтвердите своё решение.',
            'return_url': 'upload_csv'  # Ссылка на меню загрузки
        })
