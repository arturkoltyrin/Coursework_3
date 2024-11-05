import pandas as pd
import pytest

from src.reports import spending_by_category


@pytest.fixture
def transactions_data():
    """Фикстура, возвращающая тестовые данные транзакций."""
    data = {
        "Дата платежа": [
            "01.01.2023 12:00:00",
            "15.02.2023 12:00:00",
            "10.03.2023 12:00:00",
            "05.04.2023 12:00:00",
            "20.01.2023 12:00:00",
            "25.02.2023 12:00:00",
            "30.12.2023 12:00:00",
        ],
        "Категория": [
            "food",
            "food",
            "transport",
            "food",
            "entertainment",
            "transport",
            "food",
        ],
        "Сумма платежа": [100, 200, 150, 250, 300, 100, 400],
    }
    return pd.DataFrame(data)


def test_spending_by_category_no_category(transactions_data):
    result = spending_by_category(
        transactions_data, "entertainment", "05.04.2023 12:00:00"
    )
    assert isinstance(result, pd.DataFrame), "Результат должен быть DataFrame"
    assert (
        result.iloc[0, 0] == 300
    ), "Сумма по категории 'entertainment' должна быть 300"


def test_spending_by_category_past_date(transactions_data):
    result = spending_by_category(transactions_data, "food", "01.01.2023 12:00:00")
    assert isinstance(result, pd.DataFrame), "Результат должен быть DataFrame"
    assert result.iloc[0, 0] == 100, "Сумма по категории 'food' должна быть 100"


def test_spending_by_category_no_transactions(transactions_data):
    result = spending_by_category(
        transactions_data, "nonexistent", "05.04.2023 12:00:00"
    )
    assert isinstance(result, pd.DataFrame), "Результат должен быть DataFrame"
    assert result.iloc[0, 0] == 0, "Сумма должна быть 0 для несуществующей категории"


def test_spending_by_category_with_future_date(transactions_data):
    result = spending_by_category(transactions_data, "food", "30.12.2023 12:00:00")
    assert isinstance(result, pd.DataFrame), "Результат должен быть DataFrame"
    assert result.iloc[0, 0] == 400, "Сумма по категории 'food' должна быть 400"
