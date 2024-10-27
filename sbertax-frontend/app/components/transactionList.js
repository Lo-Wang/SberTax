'use client';

import { useEffect, useState } from 'react';

export default function TransactionList({ onSelectTransaction }) {
    const [transactions, setTransactions] = useState([]);
    const [selectedTransactionId, setSelectedTransactionId] = useState(null); // Состояние для выбранной транзакции

    useEffect(() => {
        // Загрузка данных из file.json
        fetch('/transactions/file.json')
            .then((response) => response.json())
            .then((data) => setTransactions(data))
            .catch((error) => console.error('Ошибка загрузки транзакций:', error));
    }, []);

    const handleTransactionClick = (transactionId) => {
        setSelectedTransactionId(transactionId); // Обновляем состояние выбранной транзакции
        onSelectTransaction(transactionId); // Вызываем функцию для передачи выбранной транзакции
    };

    return (
        <div className="transactionList">
            <h2 className="titleTran">Доступные транзакции</h2>
            <div className="scrollArea">
                {transactions.length > 0 ? (
                    transactions.map((transaction) => (
                        <div
                            key={transaction.id}
                            className={`transactionCard ${selectedTransactionId === transaction.id ? 'selected' : ''}`} // Добавляем класс для выделенной транзакции
                            onClick={() => handleTransactionClick(transaction.id)} // Обработчик клика
                        >
                            <div className="transactionDetail">
                                <strong>ID:</strong> {transaction.id}
                            </div>
                            <div className="transactionDetail">
                                <strong>Сумма:</strong> {transaction.amount} руб.
                            </div>
                            <div className="transactionDetail">
                                <strong>Категория:</strong> {transaction.category}
                            </div>
                            <div className="transactionDetail">
                                <strong>MCC Code:</strong> {transaction.mcc_code}
                            </div>
                        </div>
                    ))
                ) : (
                    <p>Транзакции не найдены</p>
                )}
            </div>
        </div>
    );
}
