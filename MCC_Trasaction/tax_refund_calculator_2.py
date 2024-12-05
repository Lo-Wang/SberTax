import csv
import re
from typing import List, Dict

# Определение допустимых MCC кодов для социального вычета (примерные категории: спортзал, секции, обучение)
ELIGIBLE_MCC_CODES = {
    "учеба": [8211, 8220, 8241],  # Образование
    "спорт": [7997, 7992, 8049],  # Спортивные клубы, фитнес
}

# MCC-коды для доходов (примерные)
INCOME_MCC_CODES = [8999, 6011, 6012]

# Ключевые слова, связанные с зарплатой (выделил что чаще всего встречается в найс банках- Сбер, Т-Банк, Альфа, ВТБ)
SALARY_KEYWORDS = [
    "зарплата", "заработная плата", "оплата труда", "аванс", "вознаграждение"
]

def load_transactions(file_path: str) -> List[Dict]:
    """
    Загружает транзакции из CSV-файла.

    :param file_path: Путь к CSV-файлу.
    :return: Список транзакций в виде словарей.
    """
    transactions = []
    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            transactions.append({
                "date": row.get("Дата операции"),
                "amount": float(row.get("Сумма", 0)),
                "mcc": int(row.get("MCC", 0)),
                "description": row.get("Описание", ""),
            })
    return transactions

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
    if transaction["mcc"] in INCOME_MCC_CODES or is_salary_comment(transaction["description"]):
        transaction["category"] = "доход"
        transaction["type"] = "income"
    else:
        transaction["category"] = "другое"
        transaction["type"] = "unknown"
    return transaction

def is_salary_comment(comment: str) -> bool:
    """
    Проверяет, содержит ли комментарий информацию о зарплате.

    :param comment: Комментарий к транзакции.
    :return: True, если это зарплатная транзакция, иначе False.
    """
    comment = comment.lower()  # Приводим к нижнему регистру
    for keyword in SALARY_KEYWORDS:
        if re.search(rf"\b{keyword}\b", comment):
            return True
    return False

def calculate_total_income(transactions: List[Dict]) -> float:
    """
    Рассчитывает общий доход по транзакциям.

    :param transactions: Список транзакций.
    :return: Общая сумма дохода.
    """
    total_income = sum(transaction["amount"] for transaction in transactions if transaction["type"] == "income")
    return round(total_income, 2)

def filter_eligible_transactions(transactions: List[Dict]) -> List[Dict]:
    """
    Фильтрует транзакции, подходящие для социального вычета.

    :param transactions: Список транзакций.
    :return: Список подходящих транзакций.
    """
    return [tx for tx in transactions if tx["category"] in ELIGIBLE_MCC_CODES]

def calculate_refund(eligible_expenses: List[Dict], total_income: float, max_refund: float = 15600) -> float:
    """
    Рассчитывает размер социального вычета.

    :param eligible_expenses: Список подходящих транзакций.
    :param total_income: Общий доход.
    :param max_refund: Максимальный размер вычета (по умолчанию 15 600 рублей).
    :return: Размер вычета.
    """
    total_expenses = sum(tx["amount"] for tx in eligible_expenses)
    refund = min(total_expenses * 0.13, total_income * 0.13, max_refund)
    return round(refund, 2)

def generate_report(eligible_expenses: List[Dict], refund: float) -> None:
    """
    Генерирует отчет по подходящим транзакциям и расчету вычета.

    :param eligible_expenses: Список подходящих транзакций.
    :param refund: Рассчитанный размер вычета.
    """
    print("\nПодходящие расходы:")
    for tx in eligible_expenses:
        print(f"- {tx['date']}: {tx['amount']} руб. ({tx['category']})")
    print(f"\nРассчитанный размер вычета: {refund:.2f} руб.")

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

# Пример вызова (как использовать, импорт, просто вызов функции и передача таблицы)
process_transactions_with_income("transactions.csv")

