from django.db import models

# Информация о модели, что работает с нашими данными
# Она основана на сокращённом датасете из ИНИД
# Источник: https://data.rcsi.science/data-catalog/datasets/160/
# От части столбцов отказались, оставшиеся см. ниже


class Settlement(models.Model):
    # Наименование субъекта РФ
    region = models.CharField(max_length=255)
    # Наименование муниципального образования
    municipality = models.CharField(max_length=255)
    # Наименование населённого пункта
    settlement = models.CharField(max_length=255)
    # Тип (город, село, деревня, кожуун, станица и др.)
    type = models.CharField(max_length=100)
    # Население населённого пункта (всего)
    population = models.IntegerField()
    # Количество детей (до 18 лет) в населённом пункте
    children = models.IntegerField()

    def __str__(self):
        return f"{self.settlement}, {self.region}"
