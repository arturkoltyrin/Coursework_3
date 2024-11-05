from datetime import datetime
from unittest.mock import patch

import pandas as pd

from src.utils import (get_data_from_excel, greeting_user, operations_cards,
                       sort_date_operations, top_five_transactions)


@patch("pandas.read_excel")
def test_get_data_from_excel(mock_read_excel):
    # Проверяем, что возвращается пустой список при ошибке
    mock_read_excel.side_effect = FileNotFoundError
    assert get_data_from_excel("dummy_path.xlsx") == []

    mock_read_excel.side_effect = None
    mock_read_excel.return_value = pd.DataFrame(
        {"Дата операции": [], "Сумма операции": []}
    )
    assert get_data_from_excel("dummy_path.xlsx") == []


# Тест для sort_date_operations
def test_sort_date_operations():
    operations = [
        {"Дата операции": "01.01.2023 12:00:00", "Сумма операции": 100},
        {"Дата операции": "15.03.2023 12:00:00", "Сумма операции": 200},
        {"Дата операции": "01.04.2023 12:00:00", "Сумма операции": 150},
    ]
    date = "2023-04-01 12:00:00"
    sorted_ops = sort_date_operations(operations, date)
    assert len(sorted_ops) == 0


# Тест для greeting_user
@patch("src.utils.datetime")
def test_greeting_user(mock_datetime):
    # Утро
    mock_datetime.now.return_value = datetime(2023, 5, 10, 5)
    assert greeting_user() == "Доброе утро"

    # День
    mock_datetime.now.return_value = datetime(2023, 5, 10, 13)
    assert greeting_user() == "Добрый день"

    # Вечер
    mock_datetime.now.return_value = datetime(2023, 5, 10, 19)
    assert greeting_user() == "Добрый вечер"

    # Ночь
    mock_datetime.now.return_value = datetime(2023, 5, 10, 1)
    assert greeting_user() == "Доброй ночи"


# Тест для operations_cards
def test_operations_cards():
    operations = [
        {"Номер карты": "1234567890123456", "Сумма операции": "$100"},
        {"Номер карты": "1234567890123456", "Сумма операции": "$250"},
        {"Номер карты": "6543210987654321", "Сумма операции": "$200"},
    ]
    result = operations_cards(operations)
    assert len(result) == 2
    assert result[0]["total_spent"] == 350  # 100 + 250
    assert result[0]["last_digits"] == "3456"


# Тест для top_five_transactions
def test_top_five_transactions():
    operations = [
        {
            "Дата операции": "01.01.2023 12:00:00",
            "Сумма операции": "$100",
            "Категория": "продукты",
            "Описание": "покупка",
        },
        {
            "Дата операции": "15.03.2023 12:00:00",
            "Сумма операции": "$200",
            "Категория": "транспорт",
            "Описание": "билет",
        },
        {
            "Дата операции": "01.04.2023 12:00:00",
            "Сумма операции": "$150",
            "Категория": "развлечения",
            "Описание": "кино",
        },
        {
            "Дата операции": "10.04.2023 12:00:00",
            "Сумма операции": "$250",
            "Категория": "путешествия",
            "Описание": "отель",
        },
        {
            "Дата операции": "15.04.2023 12:00:00",
            "Сумма операции": "$300",
            "Категория": "покупки",
            "Описание": "одежда",
        },
        {
            "Дата операции": "20.04.2023 12:00:00",
            "Сумма операции": "$400",
            "Категория": "еда",
            "Описание": "рестораны",
        },
    ]
    result = top_five_transactions(operations)
    # проверьте результат
    assert len(result) == 5
