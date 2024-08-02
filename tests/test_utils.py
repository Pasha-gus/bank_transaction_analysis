from unittest.mock import patch

import pandas as pd

from src.utils import (exchange_rates, get_actions_data, get_card_data, greeting_by_time_of_day,
                       top_transaction_payment_amount)


# Тесты функции greeting_by_time_of_day
def test_greeting_morning():
    with patch("src.utils.datetime") as mock_datetime:
        mock_datetime.now.return_value.hour = 8  # Установим время на 8 утра
        assert greeting_by_time_of_day() == "Доброе утро"


def test_greeting_day():
    with patch("src.utils.datetime") as mock_datetime:
        mock_datetime.now.return_value.hour = 14  # Установим время на 2 дня
        assert greeting_by_time_of_day() == "Добрый день"


def test_greeting_evening():
    with patch("src.utils.datetime") as mock_datetime:
        mock_datetime.now.return_value.hour = 20  # Установим время на 8 вечера
        assert greeting_by_time_of_day() == "Добрый вечер"


def test_greeting_night():
    with patch("src.utils.datetime") as mock_datetime:
        mock_datetime.now.return_value.hour = 2  # Установим время на 2 ночи
        assert greeting_by_time_of_day() == "Доброй ночи"


# Тест функции top_transaction_payment_amount
def test_top_transaction_payment_amount():
    data = {
        "Сумма платежа": [100, 200, 300, 400, 500],
        "Описание": ["Транзакция 1", "Транзакция 2", "Транзакция 3", "Транзакция 4", "Транзакция 5"],
    }
    df = pd.DataFrame(data)

    top_transactions = top_transaction_payment_amount(df)
    assert len(top_transactions) == 5
    assert top_transactions[0]["Сумма платежа"] == 500
    assert top_transactions[1]["Сумма платежа"] == 400


# Тест функции get_card_data
def test_get_card_data():
    data = {"Сумма операции": [-100, -200, -300, 100], "Номер карты": ["*3456", "*3456", "*3456", "*4444"]}
    df = pd.DataFrame(data)

    result = get_card_data(df)
    assert result[0]["Общая сумма расходов"] == -600.0
    assert result[0]["Последние 4 цифры"] == "3456"


@patch("requests.get")
def test_exchange_rates(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"query": {"from": "USD"}, "result": 75.0}
    rates = exchange_rates()
    assert len(rates) == 2
    assert rates[0]["currency"] == "USD"
    assert rates[0]["rate"] == 75.0
    mock_get.return_value.json.return_value = {"query": {"from": "EUR"}, "result": 85.0}
    rates = exchange_rates()
    assert len(rates) == 2
    assert rates[1]["currency"] == "EUR"
    assert rates[1]["rate"] == 85.0


mock_response_json = {
    "Time Series (Daily)": {
        "2023-10-01": {"1. open": "150.00", "2. high": "155.00", "3. low": "149.00", "4. close": "154.00"},
        "2023-10-02": {"1. open": "155.00", "2. high": "156.00", "3. low": "152.00", "4. close": "155.50"},
    }
}


@patch("requests.get")
def test_get_actions_data(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = mock_response_json
    result = get_actions_data()
    for stock in result["stock_prices"]:
        assert stock["price"] == 155.50
    assert len(result["stock_prices"]) == 5
