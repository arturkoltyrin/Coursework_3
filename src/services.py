import json
import re
from typing import Any, Dict, List


def transactions_by_phone_numbers(operations: List[Dict[str, Any]]) -> str:
    """Возвращает JSON со всеми транзакциями, содержащими в описании мобильные номера."""

    # Регулярное выражение для поиска мобильных номеров
    phone_pattern = re.compile(
        r"\b(?:\+7|8)?\s*(909|919|929|949|959|970|980|997|999|\d{3})\s*\d{3}\s*[-]?\s*\d{2}\s*[-]?\s*\d{2}\b"
    )

    # Фильтруем транзакции, которые содержат номера телефонов в поле "Описание"
    filtered_transactions = [
        operation
        for operation in operations
        if "Описание" in operation and phone_pattern.search(operation["Описание"])
    ]

    # Возвращаем отфильтрованные транзакции в виде JSON
    return json.dumps(filtered_transactions, ensure_ascii=False)
