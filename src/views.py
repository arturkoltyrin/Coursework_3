import json

from src.utils import (currency_rates, get_data_from_excel, greeting_user,
                       operations_cards, sort_date_operations, stock_prices,
                       top_five_transactions)


def web_main(date):
    operations = get_data_from_excel("../data/operations.xlsx")
    operations = sort_date_operations(operations, date)
    result = {
        "greeting": greeting_user(),
        "cards": operations_cards(operations),
        "top_transactions": top_five_transactions(operations),
        "currency_rates": currency_rates(),
        "stock_prices": stock_prices(),
    }

    return json.dumps(result, ensure_ascii=False)
