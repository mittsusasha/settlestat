from django.test import TestCase, Client
from django.urls import reverse
from settlestat.models import Settlement
from django.core.files.uploadedfile import SimpleUploadedFile


# Тесты для класса FileLoader, который отвечает за загрузку CSV-файлов
class FileLoaderTest(TestCase):
    # Метод setUp выполняется перед каждым тестом.
    # Здесь инициализируется клиент для отправки HTTP-запросов,
    # а также определяется URL-адрес для загрузки файлов.
    def setUp(self):
        self.client = Client()  # Создаём клиент для запросов
        self.upload_url = reverse('upload_csv')  # URL для загрузки файлов

    # Тест обработки GET-запроса на отображение формы загрузки CSV
    def test_get_request_renders_form(self):
        # Отправляем GET-запрос к FileLoader
        response = self.client.get(self.upload_url)
        # Проверяем, что сервер вернул статус 200 (успех)
        self.assertEqual(response.status_code, 200)
        # Проверяем, что используется правильный шаблон
        self.assertTemplateUsed(response, 'data_loader/upload_csv.html')
        # Убедимся, что HTML-ответ содержит тег формы
        self.assertContains(response, '<form')

    # Тест обработки корректного CSV-файла при POST-запросе
    def test_post_valid_csv_file(self):
        # Создаём содержимое тестового CSV-файла — сперва как строку
        csv_content = "region,municipality,settlement,type,population,children\nМосковская область,Красногорск,Нахабино,поселок,20000,5000\n"
        # Преобразуем содержимое в байты, так как SimpleUploadedFile требует объект bytes
        csv_bytes = csv_content.encode('utf-8')

        # Создаем тестовый файл для загрузки
        csv_file = SimpleUploadedFile(
            "test.csv",  # Имя файла
            csv_bytes,   # Содержимое файла в виде байтов
            content_type="text/csv"  # MIME-тип файла
        )

        # Отправляем POST-запрос с файлом
        response = self.client.post(
            self.upload_url, {'csv_file': csv_file}, follow=True)

        # Проверяем, что данные успешно добавлены в базу
        # Должна быть одна запись
        self.assertEqual(Settlement.objects.count(), 1)
        settlement = Settlement.objects.first()  # Получаем добавленную запись
        # Проверяем, что данные совпадают с ожиданиями
        self.assertEqual(settlement.region, "Московская область")
        self.assertEqual(settlement.municipality, "Красногорск")
        self.assertEqual(settlement.settlement, "Нахабино")
        self.assertEqual(settlement.population, 20000)
        self.assertEqual(settlement.children, 5000)
        # Убедимся, что отображается сообщение об успешной загрузке
        self.assertContains(response, "Датасет успешно загружен в базу данных")

# Тесты для класса FileRemover, который отвечает за удаление данных из базы.


class FileRemoverTest(TestCase):

    # Метод setUp создаёт тестовые данные и URL для удаления
    def setUp(self):
        # Добавляем одну запись в базу для тестов
        Settlement.objects.create(
            region="Московская область",
            municipality="Красногорск",
            settlement="Нахабино",
            type="поселок",
            population=20000,
            children=5000
        )
        self.delete_url = reverse('delete_csv')  # URL для удаления данных
        self.client = Client()  # Создаём клиент для отправки запросов

    # Тест отображения страницы подтверждения удаления данных
    def test_get_request_renders_confirmation(self):
        # Отправляем GET-запрос к FileRemover
        response = self.client.get(self.delete_url)
        # Проверяем, что сервер вернул статус 200 (успех)
        self.assertEqual(response.status_code, 200)
        # Проверяем, что используется правильный шаблон
        self.assertTemplateUsed(response, 'data_loader/delete_confirm.html')

    # Тест удаления данных при отправке POST-запроса
    def test_post_request_deletes_data(self):
        # Убедимся, что до удаления в базе есть одна запись
        self.assertEqual(Settlement.objects.count(), 1)

        # Отправляем POST-запрос на удаление данных
        response = self.client.post(self.delete_url, follow=True)

        # Проверяем, что после удаления записей в базе нет
        self.assertEqual(Settlement.objects.count(), 0)
        # Убедимся, что в ответе содержится сообщение об успешном удалении
        self.assertContains(
            response, "Данные датасета успешно удалены из базы данных")
