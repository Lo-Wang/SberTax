# Добавим категорию MCC-кодов для доходов
ELIGIBLE_MCC_CODES = {
    "учеба": [8211, 8220, 8241],  # Образование
    "спорт": [7997, 7992, 8049],  # Спортивные клубы, фитнес
}

INCOME_MCC_CODES = [8999, 6011, 6012]  #  MCC для доходов (нужно уточнить реальные, у банков зп и переводы между картами это один MCC код)

def classify_transaction(transaction: Dict) -> Dict:
    """
    Классифицирует транзакцию как расход или доход.

    :param transaction: Транзакция.
    :return: Транзакция с добавленной категорией.
    """
    for category, mcc_codes in ELIGIBLE_MCC_CODES.items():
        if transaction["mcc"] in mcc_codes:
            transaction["category"] = category
            transaction["type"] = "expense"
            return transaction
    if transaction["mcc"] in INCOME_MCC_CODES:
        transaction["category"] = "доход"
        transaction["type"] = "income"
    else:
        transaction["category"] = "другое"
        transaction["type"] = "unknown"
    return transaction


def calculate_total_income(transactions: List[Dict]) -> float:
    """
    Рассчитывает общий доход по транзакциям.

    :param transactions: Список транзакций.
    :return: Общая сумма дохода.
    """
    total_income = sum(transaction["amount"] for transaction in transactions if transaction["type"] == "income")
    return round(total_income, 2)


def process_transactions_with_income(file_path: str) -> None:
    """
    Обрабатывает транзакции, анализируя расходы, доходы и вычеты.

    :param file_path: Путь к CSV-файлу с транзакциями.
    """
    transactions = load_transactions(file_path)
    transactions = [classify_transaction(tx) for tx in transactions]

    # Выделяем доходы и расходы
    total_income = calculate_total_income(transactions)
    eligible_expenses = filter_eligible_transactions([tx for tx in transactions if tx["type"] == "expense"])

    # Рассчитываем вычет
    refund = calculate_refund(eligible_expenses, total_income)
    print(f"Общий доход: {total_income:.2f} руб.")
    generate_report(eligible_expenses, refund)
