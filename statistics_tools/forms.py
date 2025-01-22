# Форма для корректного выбора региона при просмотре статистики  
from django import forms
from settlestat.models import Settlement

class Region_selection_form(forms.Form):
    region = forms.ChoiceField(label='Выберите интересующий субъект РФ: ', choices=[])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Получаем уникальные регионы из базы данных
        regions = Settlement.objects.values_list('region', flat=True).distinct()
        # Формируем список кортежей для поля выбора
        self.fields['region'].choices = [(region, region) for region in regions]
