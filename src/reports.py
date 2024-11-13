import json
import logging
import os
from datetime import datetime
from typing import Callable, Optional

import pandas as pd

current_dir = os.path.dirname(os.path.abspath(__file__))
rel_file_path = os.path.join(current_dir, "../logs/reports.log")
abs_file_path = os.path.abspath(rel_file_path)

logger = logging.getLogger("reports")
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler(abs_file_path, "w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s - %(funcName)s %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def recording_data(file_name: str = "default_report.json") -> Callable:
    """Декоратор, который записывает в файл результат, который возвращает функция, формирующая отчет."""

    def decorator(func) -> Callable:
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            # Проверка, является ли результат числом
            if isinstance(result, (int, float)):
                with open(file_name, "w", encoding="utf-8") as f:
                    json.dump({"Сумма": result}, f, ensure_ascii=False, indent=4)
            else:
                result.to_json(path_or_buf=file_name, orient="records", force_ascii=False, indent=4)
            return result

        return wrapper

    return decorator


@recording_data("spending_report.json")
def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> float:
    """Возвращает траты по заданной категории за последние три месяца (от переданной даты)."""
    logger.info("Ищем траты по конкретной категории")
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    three_months_ago = date - pd.DateOffset(months=3)

    # Преобразование столбца "Дата платежа" в формат datetime
    transactions["Дата платежа"] = pd.to_datetime(transactions["Дата платежа"], format="%d.%m.%Y")

    # Фильтрация операций по категории и дате
    filtered_operations = transactions[
        (transactions["Категория"] == category) &
        (three_months_ago <= transactions["Дата платежа"]) &
        (transactions["Дата платежа"] <= date)
        ]

    # Возвращаем сумму операций с округлением
    total_sum = filtered_operations["Сумма операции"].sum()

    return round(total_sum, 2)
