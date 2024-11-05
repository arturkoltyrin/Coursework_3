import json
from datetime import datetime
from typing import Optional

import pandas as pd


def recording_data(file_name):
    """Декоратор, который записывает в файл результат, который возвращает функция, формирующая отчет"""

    def decorator(func):
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            with open(file_name, "w") as f:
                json.dump(result, f)
            return result

        return wrapper

    return decorator


# @recording_data('spending_report.json')
def spending_by_category(
    transactions: pd.DataFrame, category: str, date: Optional[str] = None
) -> pd.DataFrame:
    if date is None:
        date = datetime.now().strftime("%d.%m.%Y %H:%M:%S")

    date = datetime.strptime(date, "%d.%m.%Y %H:%M:%S")
    three_months_ago = date - pd.DateOffset(months=3)

    # Преобразуем 'Дата платежа' в datetime
    transactions["Дата платежа"] = pd.to_datetime(
        transactions["Дата платежа"], format="%d.%m.%Y %H:%M:%S"
    )

    # Фильтруем данные по категории и по дате
    filtered_operations = transactions[
        (transactions["Категория"] == category)
        & (three_months_ago <= transactions["Дата платежа"])
        & (transactions["Дата платежа"] <= date)
    ]

    result = filtered_operations["Сумма платежа"].sum()

    return pd.DataFrame([result])
