from django.test import TestCase, Client        # Библиотека для тестов
# Модель, которую мы будем тестировать
from settlestat.models import Settlement


# Тесты для модели Settlement — проверм корректность создания модели и взаимодействия с нею
class SettlementModelTest(TestCase):

    # Метод setUp выполняется перед каждым тестом.
    # В нём создаются тестовые данные в тестовой базе данных.
    def setUp(self):
        Settlement.objects.create(
            region="Московская область",
            municipality="Красногорск",
            settlement="Нахабино",
            type="поселок",
            population=20000,
            children=5000,
        )

    # Тест корректности создания объекта модели Settlement
    # Проверка, что данные в базе данных будут совпадать с ожидаемыми
    def test_settlement_creation(self):
        # Получаем запрашиваемый нами объект из базы данных
        settlement = Settlement.objects.get(settlement="Нахабино")
        # И проверяем его поля
        self.assertEqual(settlement.region, "Московская область")
        self.assertEqual(settlement.municipality, "Красногорск")
        self.assertEqual(settlement.population, 20000)
        self.assertEqual(settlement.children, 5000)

    # Тест на корректность строкового представления модели __str__(self)
    def test_string_representation(self):
        settlement = Settlement.objects.get(settlement="Нахабино")
        # Ожидаем получить следующее строковое представление
        self.assertEqual(str(settlement), "Нахабино, Московская область")

# Тесты для маршрутов URL данного приложения — проверка доступности страниц по их маршрутам


class URLRoutingTest(TestCase):

    # Проверка доступности главной страницы приложения
    def test_home_url_resolves(self):
        client = Client()
        # Запрашиваем главную страницу
        response = client.get("/")
        # Ожидаем получить HTTP-ответ со статусом 200
        self.assertEqual(response.status_code, 200)
