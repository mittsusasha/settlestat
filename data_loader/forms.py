# Форма для корректной работы поля, в которое пользователь будет загружать CSV-файл датасета
from django import forms


class Upload_csv_form(forms.Form):
    csv_file = forms.FileField()    # Поле для загрузки файла в формате CSV
