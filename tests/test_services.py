import pandas as pd
import json
import pytest
from src.services import profitable_categories_increased_cashback


def test_profitable_categories_increased_cashback():
    data = {
        'Дата операции': [
            '01.01.2023 12:34:56',
            '15.01.2023 09:00:00',
            '05.02.2023 15:00:00',
            '01.02.2023 10:00:00'
        ],
        'Категория': ['Еда', 'Транспорт', 'Еда', 'Транспорт'],
        'Сумма операции': [1000, -500, 2000, 800]
    }

    transactions_df = pd.DataFrame(data)

    # Тест для случая, когда мы получаем данные за январь 2023
    expected_result = json.dumps({'Еда': 1000.0, 'Транспорт': 500.0}, ensure_ascii=False)
    result = profitable_categories_increased_cashback(transactions_df, 2023, 1)
    assert result == expected_result

    # Тест для случая, когда мы получаем данные за февраль 2023
    expected_result = json.dumps({'Еда': 2000.0, 'Транспорт': 800.0}, ensure_ascii=False)
    result = profitable_categories_increased_cashback(transactions_df, 2023, 2)
    assert result == expected_result

    # Тест для пустого DataFrame
    empty_df = pd.DataFrame(columns=['Дата операции', 'Категория', 'Сумма операции'])
    expected_empty_result = json.dumps({}, ensure_ascii=False)
    result = profitable_categories_increased_cashback(empty_df, 2023, 1)
    assert result == expected_empty_result

    # Тест для месяца, в котором нет данных
    expected_no_data_result = json.dumps({}, ensure_ascii=False)
    result = profitable_categories_increased_cashback(transactions_df, 2023, 3)
    assert result == expected_no_data_result