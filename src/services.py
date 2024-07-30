import json
import logging

import pandas as pd

logger = logging.getLogger("services")
logger.setLevel(logging.INFO)
file_handler = logging.StreamHandler()
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def profitable_categories_increased_cashback(data: pd.DataFrame, year: int, month: int) -> str:
    """
    Анализирует транзакции и возвращает суммы кэшбэка по категориям за указанный месяц и год.
    Parameters:
    data (pd.DataFrame): DataFrame, содержащий данные о транзакциях.
                         Должен содержать следующие колонки:
                         - 'Дата операции': Дата и время транзакции в формате 'дд.мм.гггг чч:мм:сс'
                         - 'Сумма операции': Сумма транзакции в числовом формате (float)
                         - 'Категория': Название категории, к которой относится транзакция (строка)
    year (int): Год, за который необходимо произвести анализ (например, 2021).
    month (int): Месяц, за который необходимо произвести анализ (от 1 до 12).
    Returns:
    str: JSON-строка, содержащая словарь, где ключи — названия категорий,
         а значения — суммы кэшбэка (в положительном формате) по каждой категории.
    """
    try:
        # Преобразуем колонки "Дата операции" и "Сумма операции" в нужные типы
        data["Дата операции"] = pd.to_datetime(data["Дата операции"], format="%d.%m.%Y %H:%M:%S")
        data["Сумма операции"] = data["Сумма операции"].astype(float)

        # Фильтруем данные по указанному году и месяцу
        filtered_data = data[(data["Дата операции"].dt.year == year) & (data["Дата операции"].dt.month == month)]

        # Группируем данные по категориям и суммируем кешбэк
        analysis = filtered_data.groupby("Категория")["Сумма операции"].sum().to_dict()

        # Преобразуем суммы к положительным значениям
        analysis = {key: abs(value) for key, value in analysis.items()}

        # Возвращаем результат в формате JSON
        return json.dumps(analysis, ensure_ascii=False)
    except Exception as ex:
        logger.error(f"Произошла ошибка {ex}")
        raise ex
