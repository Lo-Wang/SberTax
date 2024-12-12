'use client';

import { useState } from 'react';
import Transaction2 from '@/app/components/transaction2';
import { useRouter } from 'next/navigation'; // Импортируем useRouter для навигации
import './styles.css'; // Стили для страницы подачи заявки

export default function ApplicationSubmission() {
    const router = useRouter(); // Создаем экземпляр роутера
    const [selectedTransactionId, setSelectedTransactionId] = useState(null);

    const handleBackClick = () => {
        router.push('/pages/dashboard');
    };


    return (
        <div className="container">
            <h1 className="title">Подходящие транзакции</h1>
            <Transaction2 />
            <div className="button-container">
                <button className="button_back" onClick={handleBackClick}>
                    <strong>Назад</strong>
                </button>
            </div>
        </div>
    );
}
