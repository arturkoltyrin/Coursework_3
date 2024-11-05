import json

import pytest

from src.services import transactions_by_phone_numbers


@pytest.fixture
def sample_operations():
    return [
        {"Описание": "Оплата по счету телефона +79091234567", "Сумма": 100},
        {"Описание": "Оплата за интернет", "Сумма": 200},
        {"Описание": "Перевод на номер 89121122334", "Сумма": 150},
        {"Описание": "Трата на продукты", "Сумма": 300},
        {"Описание": "+79991234567 перевод", "Сумма": 400},
        {"Описание": "Счет за услуги", "Сумма": 250},
    ]


def test_transactions_without_phone_numbers(sample_operations):
    # Удалим все транзакции с номерами телефонов
    operations_without_numbers = [
        {"Описание": "Оплата за интернет", "Сумма": 200},
        {"Описание": "Трата на продукты", "Сумма": 300},
        {"Описание": "Счет за услуги", "Сумма": 250},
    ]

    result = transactions_by_phone_numbers(operations_without_numbers)
    assert (
        json.loads(result) == []
    ), "Должен вернуть пустой список, если телефонные номера не найдены."


def test_empty_operations():
    # Проверьте результат с пустым списком операций
    result = transactions_by_phone_numbers([])
    assert json.loads(result) == [], "Должен вернуть пустой список для пустого ввода."
