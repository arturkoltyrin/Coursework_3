from datetime import datetime
from typing import Any
from unittest.mock import mock_open, patch

import pandas as pd
import pytest

from src.utils import (currency_rates, get_data_from_excel, stock_prices)


@patch("builtins.open", new_callable=mock_open, read_data=b"\x3c\x80\x00\x00\x00")
@patch("pandas.read_excel")
def test_get_data_from_excel(mock_read_excel: Any, mock_file: Any) -> None:
    mock_read_excel.return_value = pd.DataFrame({"amount": [100], "currency": ["USD"]})
    transactions = get_data_from_excel("data/transactions.xlsx")
    assert transactions == [{"amount": 100, "currency": "USD"}]


@patch("builtins.open", side_effect=FileNotFoundError)
def test_not_found_excel(mock_file: Any) -> None:
    transactions = get_data_from_excel("data/transactions.xlsx")
    assert transactions == []

@patch("requests.get")
def test_currency_rates(mock_convert: Any) -> None:
    mock_convert.return_value.status_code = 200
    mock_convert.return_value.json.return_value = {"data": {"RUB": {"value": 1.00}}}
    assert currency_rates() == [{"currency": "USD", "rate": 1.00}, {"currency": "EUR", "rate": 1.00}]


@patch("requests.get")
def test_stock_prices(mock_convert: Any):
    mock_convert.return_value.status_code = 200
    mock_convert.return_value.json.return_value = {"data": [{"symbol": "AAPL", "close": 1.0}]}
    assert stock_prices() == [{"stock": "AAPL", "price": 1.0}]
