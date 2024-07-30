# Проект:
Приложение для анализа банковских операций

## Описание:
Приложение анализирует информацию о банковских транзакциях из excel-файла и формерует json-данные для веб страниц

## Установка:

1. Клонируйте репозиторий:
```
git clone https://git@github.com:Pasha-gus/bank_transaction_analysis.git
```

## Использование:
Перед использованием зайдите на сайт https://apilayer.com/marketplace/exchangerates_data-api и на сайт https://www.alphavantage.co/ зарегистрируйтесь и создайте api ключи. Далее в корневой папке проекта создайте файл .env и запишите в нее информацию(шаблон для файла находится в корневой папке проекта и называется .env.example)
Чтобы пользоваться программой запустите модуль main в корневой папке проекта и следуйте указанием выводящимся в командной строке.
1. Введите дату по которой нужно искать информацию
2. Введите путь к json-файлу в который нужно создавать отчет. Если нужно сохранить путь по умолчанию то нажмите клавишу 'Enter' (файл по умолчанию /data/report.json
2. Дождитесь окончания операций
3. Введите категорию по которой нужно формеровать отчет о наиболее выгодных категориях
по умолчанию отчет записывается в файл data/report.json

## Документация:
Приложение пользуется сайтом https://apilayer.com/marketplace/exchangerates_data-api для конфертации валют и сайтом https://www.alphavantage.co/ для получения информации о стоимости акций

## Лицензия:
Этот проект лицензирован по [лицензии MIT](LICENSE).