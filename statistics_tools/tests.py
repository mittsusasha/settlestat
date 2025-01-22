from django.test import TestCase
from django.urls import reverse
from settlestat.models import Settlement
from statistics_tools.forms import Region_selection_form
from io import BytesIO
import base64

# Тесты для приложения statistics_tools


class StatisticsToolsTest(TestCase):
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
        Settlement.objects.create(
            region="Московская область",
            municipality="Истра",
            settlement="Снегири",
            type="поселок",
            population=10000,
            children=2500,
        )
        Settlement.objects.create(
            region="Тульская область",
            municipality="Тула",
            settlement="Щёкино",
            type="город",
            population=30000,
            children=8000,
        )

    # Тест фильтрации данных по региону
    def test_region_data_filter(self):
        response = self.client.post(reverse("region_data"), {
                                    "region": "Московская область"})
        self.assertEqual(response.status_code, 200)  # Успешный запрос
        # Проверяем, что в таблице отображаются только записи из выбранного региона
        self.assertContains(response, "Нахабино")
        self.assertContains(response, "Снегири")
        self.assertNotContains(response, "Щёкино")  # Запись из другого региона

    # Тест отображения графика распределения населения
    def test_population_distribution_chart(self):
        response = self.client.get(reverse("population_distribution_graph"))
        self.assertEqual(response.status_code, 200)  # Успешный запрос
        # Проверяем тип содержимого
        self.assertEqual(response["Content-Type"], "image/png")

    # Тест отображения графика зависимости детей от населения
    def test_children_vs_population_chart(self):
        response = self.client.get(reverse("children_vs_population_graph"))
        self.assertEqual(response.status_code, 200)  # Успешный запрос
        # Проверяем тип содержимого
        self.assertEqual(response["Content-Type"], "image/png")

    # Тест строки __str__ у модели Settlement (переносим для полноты тестов)
    def test_string_representation(self):
        settlement = Settlement.objects.get(settlement="Нахабино")
        self.assertEqual(str(settlement), "Нахабино, Московская область")

    # Тест корректности данных формы
    def test_region_selection_form_validation(self):
        form = Region_selection_form(data={"region": "Московская область"})
        self.assertTrue(form.is_valid())  # Данные валидны
        # Проверяем очищенные данные
        self.assertEqual(form.cleaned_data["region"], "Московская область")

    # Тест на случай, если регион не выбран
    def test_region_selection_form_no_region(self):
        form = Region_selection_form(data={"region": ""})
        self.assertFalse(form.is_valid())  # Форма должна быть невалидной
