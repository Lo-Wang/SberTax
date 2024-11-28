import csv
from typing import List, Dict

# Определение допустимых MCC кодов для социального вычета (примерные категории: спортзал, секции, обучение)
ELIGIBLE_MCC_CODES = {
    "учеба": [8211, 8220, 8241],  # Образование
    "спорт": [7997, 7992, 8049],  # Спортивные клубы, фитнес
}


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


def filter_eligible_transactions(transactions: List[Dict]) -> List[Dict]:
    """
    Отбирает транзакции, соответствующие условиям налогового вычета.

    :param transactions: Список всех транзакций.
    :return: Список транзакций, подходящих под налоговый вычет.
    """
    eligible_transactions = []
    for transaction in transactions:
        for category, mcc_codes in ELIGIBLE_MCC_CODES.items():
            if transaction["mcc"] in mcc_codes:
                transaction["category"] = category
                eligible_transactions.append(transaction)
                break
    return eligible_transactions


def calculate_refund(transactions: List[Dict]) -> float:
    """
    Рассчитывает сумму налогового вычета (13% от суммы подходящих транзакций).

    :param transactions: Список подходящих транзакций.
    :return: Сумма налогового вычета.
    """
    total_spent = sum(transaction["amount"] for transaction in transactions)
    return round(total_spent * 0.13, 2)


def generate_report(transactions: List[Dict]) -> None:
    """
    Создает отчет по подходящим транзакциям.

    :param transactions: Список подходящих транзакций.
    """
    print("Подходящие транзакции для налогового вычета:")
    for transaction in transactions:
        print(
            f"Дата: {transaction['date']}, Сумма: {transaction['amount']:.2f}, "
            f"MCC: {transaction['mcc']}, Категория: {transaction['category']}"
        )
    refund = calculate_refund(transactions)
    print(f"\nОбщая сумма налогового вычета: {refund:.2f} руб.")


# Функция для быстрого использования модуля
def process_transactions(file_path: str) -> None:
    """
    Основная функция для обработки транзакций.

    :param file_path: Путь к CSV-файлу с транзакциями.
    """
    transactions = load_transactions(file_path)
    eligible_transactions = filter_eligible_transactions(transactions)
    generate_report(eligible_transactions)
