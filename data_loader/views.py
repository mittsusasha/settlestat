# Нам нужно перетащить данные датасета из CSV-файла в нашу базу данных
# Чтобы наследовать от этого базового класса наш класс
from django.views import View
from django.shortcuts import render
from django.http import HttpResponse
from .forms import Upload_csv_form
from settlestat.models import Settlement
# Импортируем наш класс для загрузки данных из services.py
from .services import FileToDatabase


# Этот класс отображает форму загрузки
class FileLoader(View):

    # Метод для отображения данных о загрузке CSV-файла
    def post(self, request):
        form = Upload_csv_form(request.POST, request.FILES)
        if form.is_valid() and request.FILES.get('csv_file'):
            csv_file = request.FILES['csv_file']

            # Вызываем специальный метод для загрузки данных из CSV в базу данных
            # Нужно вызывать его через экземпляр класса, иначе... ошибка будет, в общем
            loader = FileToDatabase()  # Создаём экземпляр класса FileToDatabase
            # И вызываем нужный метод через его экземпляр
            result = loader.csv_to_db(csv_file)

            # Проверка на корректность у нас, конечно, слишком простая...
            # Если результат — это число, значит загрузка прошла успешно
            if isinstance(result, int):
                success_message = f"Датасет успешно загружен в базу данных приложения! Обработано записей: {
                    result}"
                return render(request, 'data_loader/upload_csv.html', {
                    'form': form,
                    'success_message': success_message,  # Передаём сообщение об успешной загрузке
                })
            else:
                # Если результат не число (строка) — значит, произошла ошибка
                return HttpResponse(result)
        else:
            # Если форма не валидна или файл не передан вообще
            return HttpResponse("Ошибка: Проблема с форматом файла!")

    # Метод для отображения формы загрузки CSV-файла в интерфейсе

    def get(self, request):
        form = Upload_csv_form()
        return render(request, 'data_loader/upload_csv.html', {
            'form': form,
            'success_message': None,
        })


# Этот класс сообщает пользователю об успешной загрузке... так ли он вообще нужен?


class UploadSuccess(View):
    def get(self, request):
        return render(request, 'data_loader/upload_success.html')


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
