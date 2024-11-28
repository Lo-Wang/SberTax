# SberTax

## Архитектура Ветки

### Основная папка с фичей - MCC_Transaction:

В папке лежит скрипт который может посчитать сумму налога за прошедший расчетный год.

Так же, там задокументированный функции и весь код можно применять через импорты:

Например:

```Python
# Импортируем все функции
from tax_refund_calculator import load_transactions, filter_eligible_transactions, calculate_refund 

# Добавояем путь к файлу с транзакциями
file_path = "transactions.csv"

# Шаг 1: Загружаем транзакции
transactions = load_transactions(file_path)

# Шаг 2: Выбираем подходящие транзакции
eligible_transactions = filter_eligible_transactions(transactions)

# Шаг 3: Рассчитываем сумму вычета
refund = calculate_refund(eligible_transactions)

# Выводим результаты результатов
print(f"Подходящих транзакций: {len(eligible_transactions)}")
for transaction in eligible_transactions:
    print(f"Дата: {transaction['date']}, Сумма: {transaction['amount']:.2f}, MCC: {transaction['mcc']}")

print(f"\nОбщая сумма налогового вычета за прошлый год: {refund:.2f} руб.")

```


