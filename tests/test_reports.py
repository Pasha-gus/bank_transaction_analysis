import pandas as pd

from src.reports import spending_by_category


def test_spending_by_category_valid_data(sample_data):
    """Тест на корректный расчет расходов по категории."""
    result = spending_by_category(sample_data, "food", "30.09.2023")
    expected = [{"Категория": "food", "Общие траты": 750.0}]
    assert result == expected


def test_spending_by_category_empty_category(sample_data):
    """Тест на ситуацию, когда нет расходов по указанной категории."""
    result = spending_by_category(sample_data, "unknown_category", "30.09.2023")
    assert result == []


def test_spending_by_category_missing_column():
    """Тест на обработку случая, когда отсутствует необходимый столбец."""
    data = {"Дата платежа": ["01.09.2023", "15.09.2023"], "Сумма операции": [300, 150]}
    df_missing_column = pd.DataFrame(data)
    result = spending_by_category(df_missing_column, "Food", "30.09.2023")
    assert result == []


def test_spending_by_category_invalid_date_format(sample_data):
    """Тест на обработку неверного формата даты."""
    result = spending_by_category(sample_data, "food", "invalid_date")
    assert result == []


def test_spending_by_category_no_transactions(sample_data):
    """Тест на случай, если DataFrame пустой."""
    empty_df = pd.DataFrame(columns=["Категория", "Дата платежа", "Сумма операции"])
    result = spending_by_category(empty_df, "Food", "30.09.2023")
    assert result == []
