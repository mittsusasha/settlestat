# Вынесем реализацию загрузки данных из CSV-файла в сервисный слой

import pandas as pd
from settlestat.models import Settlement

# Этот класс используется для загрузки файлов (пока что только в формате CSV)


class FileToDatabase:
    # Метод для загрузки данных из CSV файла в базу данных приложения
    def csv_to_db(self, csv_file):       # Возможно, не лучшее решение из возможных

        try:    # Работу с файлами положено оборачивать в try/catch
            # Чтение CSV файла с помощью pandas
            df = pd.read_csv(csv_file)

            # Преобразование данных и сохранение в базу данных
            for _, row in df.iterrows():
                # Создаем запись в базе данных для каждого ряда из CSV
                Settlement.objects.create(
                    region=row['region'],
                    municipality=row['municipality'],
                    settlement=row['settlement'],
                    type=row['type'],
                    population=row['population'],
                    children=row['children']
                )

            # Возвращаем количество успешно обработанных записей
            # Минимальная проверка на корректность работы
            # Предположим, что если мы отдали хоть что-то, то значит, прочитали файл корректно
            return len(df)

        # Пробуем поймать ошибку, если она возникла в нашем try
        except Exception as e:
            # И в случае ошибки возвращаем её описание волшебной f-строкой
            return f"При загрузке данных произошла ошибка: {str(e)}"
