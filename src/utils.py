import logging
from datetime import datetime
import requests
from dotenv import load_dotenv
import os
import pandas as pd


load_dotenv()
api_key_currency = os.getenv("APILAYER_API_KEY")
api_key_actions = os.getenv("ALPHA_VANTAGE_API_KEY")


logger = logging.getLogger("utils")
logger.setLevel(logging.INFO)
file_handler = logging.StreamHandler()
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def transaction_data_excel(path_file: str) -> list:
    try:
        logger.info(f"Считываем содержимое файла {path_file}")
        excel_data = pd.read_excel(path_file)
        return excel_data
    except FileNotFoundError:
        logger.error(f"Ошибка: Файл {path_file} не найден")
        raise
    except ValueError as ex:
        logger.error(f"Ошибка: {ex} неправильный формат файла")
        raise
    except Exception as ex:
        logger.error(f"Ошибка: {ex}")
        raise


def greeting_by_time_of_day():
    """
    Возвращает приветствие в зависимости от текущего времени суток.
    - "Доброе утро" для утра (с 4:00 до 11:59)
    - "Добрый день" для дня (с 12:00 до 17:59)
    - "Добрый вечер" для вечера (с 18:00 до 23:59)
    - "Доброй ночи" для ночи (с 0:00 до 3:59)
    """
    today_date = datetime.now()
    if 4 <= today_date.hour < 12:
        return "Доброе утро"
    elif 12 <= today_date.hour < 18:
        return "Добрый день"
    elif 18 <= today_date.hour < 24:
        return "Добрый вечер"
    else:
        return "Доброй ночи"




def top_transaction_payment_amount(transactions_df: pd.DataFrame) -> list[dict]:
    """
    Возвращает топ-5 транзакций с наибольшими суммами платежей.
    Параметры:
    transactions_df (pd.DataFrame): DataFrame транзакций, который должен содержать
                                     как минимум столбец "Сумма платежа".
    Возвращает:
    list[dict]: Список словарей, содержащий топ-5 транзакций, отсортированных по сумме платежа.
    """
    if transactions_df.empty:
        return []
    # Сортировка DataFrame по столбцу "Сумма платежа" в порядке убывания и получение топ-5
    top_transactions_df = transactions_df.sort_values(by="Сумма платежа", ascending=False).head(5)
    # Преобразование DataFrame в список словарей
    return top_transactions_df.to_dict(orient='records')





def exchange_rates():
    currency_list = ["USD", "EUR"]
    currency_rates = []

    for currency in currency_list:
        url = f"https://api.apilayer.com/exchangerates_data/convert?to=RUB&from={currency}&amount=1"

        headers = {
            "apikey": api_key_currency
        }

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            result = response.json()  # Парсим JSON-ответ
            currency_info = {
                "currency": result["query"]["from"],  # Здесь получаем код валюты
                "rate": result["result"],  # Здесь получаем курс
            }
            currency_rates.append(currency_info)  # Добавляем информацию о валюте в список
        else:
            raise ValueError(f"Не удалось получить обменный курс, статус код: {response.status_code}")

    return currency_rates



def get_card_data(df: pd.DataFrame) -> list[dict]:
    """
    Получает данные о расходах с карт и рассчитывает кешбэк по последним 4 цифрам номера карты.
    Параметры:
    df (pd.DataFrame): DataFrame, содержащий колонки 'Сумма операции' и 'Номер карты'.
    Возвращает:
    list[dict]: Список словарей с общей суммой расходов и кешбэком для каждой карты.
    """
    # Преобразуем колонки с суммами в числовой формат
    df['Сумма операции'] = df['Сумма операции'].astype(str).str.replace(',', '.', regex=False).astype(float)
    expenses_df = df[df['Сумма операции'] < 0].copy()
    # Извлекаем последние 4 цифры номера карты
    expenses_df['Последние 4 цифры'] = expenses_df['Номер карты'].str.extract('(\d{4})', expand=False)
    # Группируем по последним 4 цифрам карты и суммируем расходы
    cashback_df = (
        expenses_df.groupby('Последние 4 цифры', as_index=False)
        .agg({'Сумма операции': 'sum'})
    )
    # Рассчитываем кешбэк (1 рубль на каждые 100 рублей)
    cashback_df['Кешбэк'] = (cashback_df['Сумма операции'].abs() // 100).astype(int)
    # Переименовываем колонки для ясности
    cashback_df.rename(columns={'Сумма операции': 'Общая сумма расходов'}, inplace=True)
    # Возвращаем список словарей
    return cashback_df.to_dict(orient='records')





def get_actions_data():
    actions = ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]
    stock_prices = []

    for action in actions:
        url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={action}&apikey={api_key_actions}"
        response = requests.get(url)

        if response.status_code == 200:
            result = response.json()  # Парсим JSON-ответ

            # Извлекаем нужные данные
            if "Time Series (Daily)" in result:
                daily_data = result["Time Series (Daily)"]
                # Получаем самую последнюю дату
                latest_date = max(daily_data.keys())
                closing_price = daily_data[latest_date]['4. close']
                stock_prices.append({
                    "stock": action,
                    "price": float(closing_price)  # Преобразуем в float для удобства
                })
            else:
                print(f"Ошибка получения данных. {action}: {result.get('Error Message')}")
        else:
            print(f"Не удалось получить данные для {action}: HTTP {response.status_code}")

    return {"stock_prices": stock_prices}
