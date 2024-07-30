import json
import logging
import os
from datetime import datetime
from typing import Any, Callable, Optional

import pandas as pd

logger = logging.getLogger("reports")
logger.setLevel(logging.INFO)
file_handler = logging.StreamHandler()
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def report_to_file(filename: Optional[str] = None):
    """
    Декоратор для записи результатов функции-отчета в файл в формате JSON.
    Параметры:
    - filename: Имя файла для записи отчета (если None, используется имя по умолчанию).
    """

    def decorator(func: Callable[[Any], Any]) -> Callable[[Any], Any]:
        def wrapper(*args, **kwargs):
            try:
                report_data = func(*args, **kwargs)
                if filename:
                    filename_to_use = filename
                    os.makedirs(os.path.dirname(filename_to_use), exist_ok=True)
                else:
                    filename_to_use = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data/report.json")
                    os.makedirs(os.path.dirname(filename_to_use), exist_ok=True)
                if report_data:
                    with open(filename_to_use, "w", encoding="utf-8") as f:
                        json.dump(report_data, f, ensure_ascii=False, indent=4)
                    print(f"Отчет сохранен в файл: {filename_to_use}")
                else:
                    logger.warning("Нет данных для записи в файл.")
                return report_data
            except Exception as ex:
                logger.error(f"Ошибка при создании отчета: {ex}")
                return []

        return wrapper

    return decorator


@report_to_file()
def spending_by_category(
    transactions: pd.DataFrame, category: str, date: Optional[str] = None
) -> list[dict[str, Any]]:
    # Проверяем наличие необходимых столбцов
    required_columns = ["Категория", "Дата платежа", "Сумма операции"]
    for col in required_columns:
        if col not in transactions.columns:
            logger.error(f"Отсутствует необходимый столбец: {col}")
            return []
    # Если дата не передана, используем текущую дату
    if date is None:
        date = datetime.now()
    else:
        try:
            date = pd.to_datetime(date, format="%d.%m.%Y")
        except ValueError:
            logger.error("Неверный формат даты. Ожидается: ДД.ММ.ГГГГ.")
            return []
    # Получаем дату трёхмесячной давности
    three_months_ago = date - pd.DateOffset(months=3)
    # Фильтруем транзакции по категории и по дате
    transactions["Дата платежа"] = pd.to_datetime(transactions["Дата платежа"], format="%d.%m.%Y", errors="coerce")
    filtered_transactions = transactions[
        (transactions["Категория"] == category.capitalize())
        & (transactions["Дата платежа"] >= three_months_ago)
        & (transactions["Дата платежа"] <= date)
    ]
    # Проверяем, есть ли транзакции после фильтрации
    if filtered_transactions.empty:
        logger.warning(f"Нет транзакций для категории '{category}' за указанный период.")
        return []
    # Суммируем траты по выбранной категории
    total_spending = filtered_transactions["Сумма операции"].sum()
    # Возвращаем список словарей с результатами
    return [{"Категория": category, "Общие траты": float(total_spending)}]
