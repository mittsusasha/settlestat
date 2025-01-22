# Различные функции для работы со статистикой
import matplotlib.pyplot as plt
from .forms import Region_selection_form
import pandas as pd
from settlestat.models import Settlement
from django.http import HttpResponse
from io import BytesIO
import seaborn as sns
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


# График для изучения распределения населения по регионам — визуализация с использованием MatplotLib и Seaborn


def population_distribution(request):
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
    plt.figure(figsize=(15, 8))     # Сделал побольше, для читаемости
    # errorbar=None, убрали доверительный интервал, тут он не нужен
    sns.barplot(x='region', y='population', data=df_sorted, errorbar=None)
    plt.yscale('log')  # Устанавливаем логарифмическую шкалу для оси Y
    # Развернём подписи на оси X для наглядности
    plt.xticks(rotation=90, fontsize=10)
    plt.title(
        'Распределение населения по регионам (для наглядности используется логарифмическая шкала)')
    plt.ylabel('Население, человек', fontsize=12)  # Подпись к оси Y
    plt.xlabel('')  # Подпись к оси X уберём, там и так подписаны регионы

    # Сохраняем получившийся график в буфер
    buf = BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close()

    # Отправляем изображение пользователю как HTTP-ответ
    return HttpResponse(buf, content_type='image/png')


# График для изучения зависимости числа детей от населения  — визуализация с использованием MatplotLib и Seaborn


def children_vs_population(request):
    # Извлекаем данные датасета из базы данных приложения
    settlements = Settlement.objects.all().values('population', 'children')
    df = pd.DataFrame(list(settlements))

    # Создаём соответствующий график
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x='population', y='children', data=df)
    plt.title('Зависимость числа детей в населённых пунктах от их общего населения')

    plt.ylabel('Дети до 18 лет, человек', fontsize=12)  # Подпись к оси Y
    plt.xlabel('Общее население, человек', fontsize=12)  # Подпись к оси X

    # И сохраняем получившийся в результате график в буфер
    buf = BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close()

    # Отправляем изображение пользователю как HTTP-ответ
    return HttpResponse(buf, content_type='image/png')

# Представление непосредственно для отображения графика распределения населения по регионам


def show_population_distribution(request):
    return render(request, 'statistics_tools/population_distribution.html')

# Представление непосредственно для отображения графика зависимости числа детей от населения


def show_children_vs_population(request):
    return render(request, 'statistics_tools/children_vs_population.html')


# Обработка выбора региона и показ данных для выбранного пользователем региона


def region_data(request):
    # Обрабатываем форму выбора региона, если он был выбран пользователем (пришёл в запросе POST)
    if request.method == 'POST':
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
            (total_children / total_population) * 100, 2) if total_population else 0    # Чтобы не делить на ноль

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

    # Иначе показываем форму для выбора региона (если пришёл запрос GET на её получение)
    return render(request, 'statistics_tools/region_data.html', {
        'regions': Settlement.objects.values_list('region', flat=True).distinct().order_by('region'),
        'settlements': None,
        'selected_region': None,
    })

# Кстати, .order_by('region' в GET- и POST- запросах сортирует регионы в алфавитном порядке для всплывающего меню
