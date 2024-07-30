import json
import pandas as pd
import logging
from src.utils import greeting_by_time_of_day, top_transaction_payment_amount, exchange_rates, get_card_data, get_actions_data, transaction_data_excel

logger = logging.getLogger("views")
logger.setLevel(logging.INFO)
file_handler = logging.StreamHandler()
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def main_views(transactions_df: pd.DataFrame) -> str:
    """
    Главная функция, которая принимает дату и время, а также DataFrame транзакций и возвращает JSON-ответ.
    """
    greeting = greeting_by_time_of_day()
    logger.info("Получаем данные по катрам")
    card_data = get_card_data(transactions_df)
    logger.info("Cоставляем топ транзакций по сумме платежа")
    top_transactions = top_transaction_payment_amount(transactions_df)
    logger.info("Получаем курс валют")
    currency_rates = exchange_rates()
    logger.info("Получаем стоимость акций")
    stock_prices = get_actions_data()

    result = {
        "greeting": greeting,
        "card_data": card_data,
        "top_transactions": top_transactions,
        "currency_rates": currency_rates,
        "stock_prices": stock_prices
    }

    return json.dumps(result, ensure_ascii=False, indent=4)
