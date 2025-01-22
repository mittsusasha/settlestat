from django.urls import path
from . import views

urlpatterns = [
    path(
        'population_distribution/',
        views.show_population_distribution,
        name='population_distribution_page'
    ),
    path(
        'children_vs_population/',
        views.show_children_vs_population,
        name='children_vs_population_page'
    ),
    path(
        'population_distribution/graph/',
        views.population_distribution,
        name='population_distribution_graph'
    ),
    path(
        'children_vs_population/graph/',
        views.children_vs_population,
        name='children_vs_population_graph'
    ),
    path(
        'region_data/',
        views.region_data,
        name='region_data'
    ),
]
