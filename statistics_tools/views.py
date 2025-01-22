# Различные функции для работы со статистикой — основная функциональность приложения
# Чтобы наследовать от этого базового класса наш класс
from django.views import View
import matplotlib.pyplot as plt
from .forms import Region_selection_form
import pandas as pd
from settlestat.models import Settlement
from django.http import HttpResponse
from io import BytesIO
import seaborn as sns
from .decorators import AddWatermark
from django.shortcuts import render
from django.db.models import Sum, Count
import matplotlib
matplotlib.use('Agg')  # Используем бэкенд Agg без графического интерфейса
# Он не может выводить данные на экран, только писать в файлы
# Но для веб-приложения его хватит, в нём Django выведет изображения корректно
# см. подробности на https://matplotlib.org/stable/users/explain/figure/backends.html

# Такое решение обусловлено ошибкой TclError, возникшей при отладке кода
# Can't find a usable init.tcl in the following directories... This probably means that Tcl wasn't installed properly.
# Это можно было решить внесением изменений в скрипт, расположенный в Scripts\activate.bat
# см. https://stackoverflow.com/questions/15884075/tkinter-in-a-virtualenv
# Но я посчитал такое решение недостаточно надёжным с точки зрения переносимости (возможно, ошибочно)


# Воспользуемся паттерном Фабричный метод
# Пусть у нас будет базовый класс для классов построения различных графиков
class FactoryGraph(View):
    watermark = AddWatermark()  # Декоратор для создания водяного знака

    def create_graph(self):
        raise NotImplementedError(
            'Этот метод нужно переопределять в подклассах!')

    def get(self, request):
        # Мы будем использовать наш фабричный метод для создания графиков... любых графиков.
        buf = BytesIO()
        graph = self.create_graph()      # Создаем график
        graph = self.watermark(graph)    # И лепим на него водяной знак
        graph.tight_layout()
        graph.savefig(buf, format='png')
        buf.seek(0)
        plt.close(graph)
        return HttpResponse(buf, content_type='image/png')

# График для изучения распределения населения по регионам — визуализация с использованием MatplotLib и Seaborn
class PopulationDistribution(FactoryGraph):

    def create_graph(self):
        # Извлекаем данные датасета из базы данных приложения
        settlements = Settlement.objects.all().values('region', 'population')
        df = pd.DataFrame(list(settlements))

        # Сперва хотел обойтись строчкой ниже, но здесь не тот случай — мы ведь агрегируем данные из муниципалитетов
        # df = df.sort_values(by='population')

        # Сперва сгруппируем данные по регионам, суммируем население в каждом из них
        df_grouped = df.groupby('region', as_index=False).sum()

        # И только теперь отсортируем данные по возрастанию для большей наглядности нашего графика
        df_sorted = df_grouped.sort_values(by='population')

        # Создаём соответствующий график — с логарифмической шкалой, иначе Москва и Петербург слишком велики
        # Сделал побольше, для читаемости
        graph, ax = plt.subplots(figsize=(15, 8))
        # errorbar=None, убрали доверительный интервал, тут он не нужен
        sns.barplot(x='region', y='population', data=df_sorted, errorbar=None)
        ax.set_yscale('log')  # Устанавливаем логарифмическую шкалу для оси Y
        # Развернём подписи на оси X для наглядности
        plt.xticks(rotation=90, fontsize=10)
        ax.set_title(
            'Распределение населения по регионам (для наглядности используется логарифмическая шкала)')
        ax.set_ylabel('Население, человек', fontsize=12)  # Подпись к оси Y
        # Подпись к оси X уберём, там и так подписаны регионы
        ax.set_xlabel('')

        # Отправляем график пользователю
        return graph


# График для изучения зависимости числа детей от населения  — визуализация с использованием MatplotLib и Seaborn
class ChildrenVsPopulation(FactoryGraph):
    def create_graph(self):
        # Извлекаем данные датасета из базы данных приложения
        settlements = Settlement.objects.all().values('population', 'children')
        df = pd.DataFrame(list(settlements))

        # Создаём соответствующий график
        graph, ax = plt.subplots(figsize=(10, 6))
        sns.scatterplot(x='population', y='children', data=df)
        ax.set_title(
            'Зависимость числа детей в населённых пунктах от их общего населения')

        ax.set_ylabel('Дети до 18 лет, человек',
                      fontsize=12)  # Подпись к оси Y
        ax.set_xlabel('Общее население, человек',
                      fontsize=12)  # Подпись к оси X

        # Отправляем график пользователю
        return graph


# Класс представления для отображения графиков
class ShowPopulationGraph(View):
    template_name = None    # Для переиспользования шаблон здесь указывать не будем
    # Пусть он потом указывается в наследнике или в маршруте

    def get(self, request, *args, **kwargs):
        if self.template_name is None:
            raise ValueError(
                'Для отображения графика нужно задать аттрибут template_name !')
        return render(request, self.template_name)


# Обработка выбора региона и показ данных для выбранного пользователем региона
class RegionData(View):
    # Показываем (пустую) форму для выбора региона, если пришёл запрос GET на её получение
    def get(self, request, *args, **kwargs):
        return render(request, 'statistics_tools/region_data.html', {
            'regions': Settlement.objects.values_list('region', flat=True).distinct().order_by('region'),
            'settlements': None,
            'selected_region': None,
        })

    # Обрабатываем форму выбора региона, если он был выбран пользователем (пришёл в запросе POST)
    def post(self, request, *args, **kwargs):
        selected_region = request.POST.get('region')
        # Выборку населённых пунктов производим с сортировкой по населению (по убыванию) для большей наглядности
        settlements = Settlement.objects.filter(
            region=selected_region).order_by('-population')

        # Считаем агрегированные данные из базы данных приложения
        total_population = settlements.aggregate(
            Sum('population'))['population__sum']
        total_children = settlements.aggregate(Sum('children'))[
            'children__sum']
        # Выводим только уникальные названия муниципалитетов (без дубликатов) и отсортируем их по алфавиту для удобства
        municipalities = sorted(set(settlements.values_list(
            'municipality', flat=True).distinct()))
        # municipalities = settlements.values('municipality').distinct() — так будут дубликаты названий
        # Что странно, distinct ведь... Но множество set, однако, будет состоять из уникальных элементов по определению
        # Здесь нужен .len(), а не .count(), так как это объект list (множество)
        total_municipalities = len(municipalities)
        total_settlements = settlements.count()
        children_percentage = round(
            # Чтобы не делить на ноль
            (total_children / total_population) * 100, 2) if total_population else 0

        # Форматируем числа с разделением тысяч пробелами для улучшения читаемости (см. ниже)
        formatted_settlements = []
        for settlement in settlements:
            formatted_settlements.append({
                'settlement': settlement.settlement,
                'municipality': settlement.municipality,
                'type': settlement.type,
                'population': f"{settlement.population:,}".replace(",", " ") if settlement.population else "0",
                'children': f"{settlement.children:,}".replace(",", " ") if settlement.children else "0"
            })

        # Передаем данные в шаблон согласно выбранному региону
        return render(request, 'statistics_tools/region_data.html', {
            'regions': Settlement.objects.values_list('region', flat=True).distinct().order_by('region'),
            'selected_region': selected_region,
            # Передаём в таблицу данные о населённых пунктах в отформатированном виде (см. выше)
            'settlements': formatted_settlements,
            # Отделяем тысячи пробелами для читаемости
            # .format() тут не прокатит, потому что это int, так что используем всемогущие f-строки
            'total_population': f"{total_population:,}".replace(",", " ") if total_population else "0",
            'total_children': f"{total_children:,}".replace(",", " ") if total_children else "0",
            'total_municipalities': total_municipalities,
            'total_settlements': total_settlements,
            'children_percentage': children_percentage,
            'municipalities': municipalities,
        })

# Кстати, .order_by('region' в GET- и POST- запросах сортирует регионы в алфавитном порядке для всплывающего меню
