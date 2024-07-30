import json
import logging
import os.path
from datetime import datetime
from typing import Optional

from src.reports import report_to_file, spending_by_category
from src.services import profitable_categories_increased_cashback
from src.utils import transaction_data_excel
from src.views import main_views

logger = logging.getLogger("main")
logger.setLevel(logging.INFO)
file_handler = logging.StreamHandler()
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def main(date: str, patch_file: Optional[str] = None) -> json:
    if patch_file is None:
        path_file = os.path.join(os.path.dirname(__file__), "data", "operations.xlsx")
    open_file = transaction_data_excel(path_file)
    views = main_views(open_file)
    data_datetime = datetime.strptime(date, "%d.%m.%Y")
    servises = profitable_categories_increased_cashback(open_file, data_datetime.year, data_datetime.month)
    category = input("Выберите категорию по которой нужно формеровать отчет 'Траты по категориям': ")
    logger.info("Формеруем отчеты")
    reports = (spending_by_category(open_file, category, date), report_to_file(path_file))
    result = {"views": views, "servises": servises, "reports": reports}
    print(result)


if __name__ == "__main__":
    date = input("Введите дату для получения информации: ")
    path_file = input(
        """Введите путь к json-файлу в который нужно создавать отчет. Если нужно сохранить путь по умолчанию то нажмите
        клавишу 'Enter' (файл по умолчанию /data/report.json"""
    )
    if not path_file:
        path_file = None
    main(date)
