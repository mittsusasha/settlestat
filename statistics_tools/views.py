# Различные функции для работы со статистикой
from django.shortcuts import render
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
from django.http import HttpResponse
from settlestat.models import Settlement
import pandas as pd
from .forms import Region_selection_form


# График для изучения распределения населения по регионам — визуализация с использованием MatplotLib и Seaborn


def population_distribution(request):
    # Извлекаем данные датасета из базы данных приложения
    settlements = Settlement.objects.all().values('region', 'population')
    df = pd.DataFrame(list(settlements))

    # Создаём соответствующий график
    plt.figure(figsize=(10, 6))
    sns.barplot(x='region', y='population', data=df)
    plt.xticks(rotation=90)
    plt.title('Распределение населения по регионам')

    # И сохраняем получившийся в результате график в буфер
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
    plt.title('Зависимость числа детей от населения')

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
    # Переменная для вывода данных по региону
    region_data = None

    if request.method == 'POST':
        # Обрабатываем форму выбора региона
        form = Region_selection_form(request.POST)
        if form.is_valid():             # Если форма не пустая, то...
            selected_region = form.cleaned_data['region']
            # ...получаем данные для выбранного региона
            region_data = Settlement.objects.filter(region=selected_region)
    else:
        form = Region_selection_form()    # Иначе показываем форму для выбора региона

    return render(request, 'statistics_tools/region_data.html', {
        'form': form,
        'region_data': region_data
    })
