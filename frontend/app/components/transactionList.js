'use client';

import { useEffect, useState } from 'react';
import styles from './transactionList.module.css';

export default function TransactionList({ onSelectTransaction }) {
    const [transactions, setTransactions] = useState([]);
    const [selectedTransaction, setSelectedTransaction] = useState(null);

    useEffect(() => {
        fetch('/transactions/file.json')
            .then((response) => response.json())
            .then((data) => setTransactions(data))
            .catch((error) => console.error('Ошибка загрузки транзакций:', error));
    }, []);

    const handleTransactionClick = (transaction) => {
        setSelectedTransaction(transaction);
        onSelectTransaction(transaction); // Передаем весь объект транзакции
    };

    return (
        <div className={styles.transactionList}>
            <div className={styles.scrollArea}>
                {transactions.length > 0 ? (
                    transactions.map((transaction) => (
                        <div
                            key={transaction.id}
                            className={`${styles.transactionCard} ${
                                selectedTransaction?.id === transaction.id ? styles.selected : ''
                            }`}
                            onClick={() => handleTransactionClick(transaction)}
                        >
                            <p className={styles.transactionDate}>
                                {new Date(transaction.date).toLocaleDateString('ru-RU', {
                                    year: 'numeric',
                                    month: 'long',
                                    day: 'numeric',
                                })}
                            </p>
                            <div className={styles.transactionDetails}>
                                <span>{transaction.description}</span>
                                <span>{transaction.amount.toLocaleString('ru-RU')}₽</span>
                            </div>
                            <p className={styles.transactionCategory}>{transaction.category}</p>
                        </div>
                    ))
                ) : (
                    <p>Транзакции не найдены</p>
                )}
            </div>
        </div>
    );
}
