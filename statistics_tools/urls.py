from django.urls import path
from .views import (
    PopulationDistribution,
    ChildrenVsPopulation,
    ShowPopulationDistribution,
    ShowChildrenVsPopulation,
    RegionData
)

urlpatterns = [

    # Страницы с использованием этих графиков (в формате HTML)
    path(
        'population_distribution/',
        ShowPopulationDistribution.as_view(),
        name='population_distribution_page'
    ),
    path(
        'children_vs_population/',
        ShowChildrenVsPopulation.as_view(),
        name='children_vs_population_page'
    ),

    # Графики распределения населения и числа детей (в формате PNG)
    path(
        'population_distribution/graph/',
        PopulationDistribution.as_view(),
        name='population_distribution_graph'
    ),
    path(
        'children_vs_population/graph/',
        ChildrenVsPopulation.as_view(),
        name='children_vs_population_graph'
    ),

    # Страница с просмотром данных по выбранному региону
    path(
        'region_data/',
        RegionData.as_view(),
        name='region_data'
    ),
]
