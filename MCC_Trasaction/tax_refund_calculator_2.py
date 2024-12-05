import csv
from typing import List, Dict

# Определеним допустимых MCC кодов для социального вычета (категории: спортзал, секции, обучение)
ELIGIBLE_MCC_CODES = {
    "учеба": [8211, 8220, 8241],  # Образование
    "спорт": [7997, 7992, 8049],  # Спортивные клубы, фитнес
}

# Максимальная сумма налогового вычета
MAX_REFUND = 15600  # 13% от 120 000 рублей


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


def calculate_refund(transactions: List[Dict], income: float) -> float:
    """
    Рассчитывает сумму налогового вычета (13% от суммы подходящих транзакций),
    с учетом максимальной суммы вычета и дохода пользователя.

    :param transactions: Список подходящих транзакций.
    :param income: Доход пользователя за год.
    :return: Сумма налогового вычета.
    """
    total_spent = sum(transaction["amount"] for transaction in transactions)
    potential_refund = total_spent * 0.13

    # Ограничение по доходу: возврат налога не может превышать уплаченный налог
    max_refund_by_income = income * 0.13

    # Возвращаем минимальное значение из возможного возврата
    return round(min(potential_refund, max_refund_by_income, MAX_REFUND), 2)


def generate_report(transactions: List[Dict], refund: float) -> None:
    """
    Создает отчет по подходящим транзакциям и возможному вычету.

    :param transactions: Список подходящих транзакций.
    :param refund: Сумма налогового вычета.
    """
    print("Подходящие транзакции для налогового вычета:")
    for transaction in transactions:
        print(
            f"Дата: {transaction['date']}, Сумма: {transaction['amount']:.2f}, "
            f"MCC: {transaction['mcc']}, Категория: {transaction['category']}"
        )
    print(f"\nОбщая сумма налогового вычета: {refund:.2f} руб.")


def check_eligibility(income: float) -> bool:
    """
    Проверяет, достаточно ли дохода для получения налогового вычета.

    :param income: Доход пользователя за год.
    :return: True, если пользователь может претендовать на вычет, иначе False.
    """
    return income * 0.13 > 0


# Функция для быстрого использования модуля
def process_transactions(file_path: str, income: float) -> None:
    """
    Основная функция для обработки транзакций и анализа налогового вычета.

    :param file_path: Путь к CSV-файлу с транзакциями.
    :param income: Доход пользователя за год.
    """
    if not check_eligibility(income):
        print("Доход недостаточен для получения налогового вычета.")
        return

    transactions = load_transactions(file_path)
    eligible_transactions = filter_eligible_transactions(transactions)
    refund = calculate_refund(eligible_transactions, income)
    generate_report(eligible_transactions, refund)
