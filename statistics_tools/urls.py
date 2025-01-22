from django.urls import path
from . import views

urlpatterns = [
    path('population_distribution/', views.show_population_distribution,
         name='population_distribution.html'),
    path('children_vs_population/', views.show_children_vs_population,
         name='children_vs_population.html'),
    path('population_distribution/graph/',
         views.population_distribution, name='population_distribution'),
    path('children_vs_population/graph/',
         views.children_vs_population, name='children_vs_population'),
    path('region_data/', views.region_data, name='region_data'),
]
