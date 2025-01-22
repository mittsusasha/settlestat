from django.shortcuts import render
from django.views.generic.base import View

from .models import Settlement


class Settlements_first_view(View):
    def get(self, request):
        # Не будем загружать для первого взгляда большую таблицу целиком, это слишком накладно
        # возьмём срез из 10 первых записей
        first_settlements = Settlement.objects.all()[:10]

        # Но узнать, сколько в таблце всего записей, было бы полезно
        settlements_count = Settlement.objects.count()

        # И рассчитаем, сколько в таблице осталось записей, не показанных выше
        settlements_left = settlements_count - len(first_settlements)

        # Добавим данные в контекст
        context = {
            'first_settlements': first_settlements,
            'settlements_left': settlements_left,
        }

        # Передадим полученные данные в шаблон через контекст
        return render(request, 'settlestat/settlements.html', context)
