'use client';

import { useState } from 'react';
import TransactionList from '@/app/components/transactionList'; // Компонент для отображения транзакций
import DownloadTemplateButton from '@/app/components/downloadTemplateButton'; // Кнопка для скачивания шаблона
import UploadImageButton from '@/app/components/uploadImageButton'; // Кнопка для загрузки изображения
import ContinueButton from '@/app/components/continueButton'; // Кнопка "Продолжить"
import { useRouter } from 'next/navigation'; // Импортируем useRouter для навигации

export default function ApplicationSubmission() {
    const router = useRouter(); // Создаем экземпляр роутера
    const [selectedFile, setSelectedFile] = useState(null); // Состояние для загруженного файла
    const [selectedTransactionId, setSelectedTransactionId] = useState(null);

    // Функция для обработки загруженного файла
    const handleFileUpload = (file) => {
        setSelectedFile(file);
    };

    const handleBackClick = () => {
        router.push('/pages/dashboard');
    };

    const handleTransactionSelect = (transactionId) => {
        console.log("Выбрана транзакция с ID:", transactionId);
        setSelectedTransactionId(transactionId);
    };

    return (
        <div className="container">
            <h2>Подача заявления</h2>
            <div className="buttonContainer">
                {/* Компонент для отображения транзакций */}
                <TransactionList onSelectTransaction={handleTransactionSelect} selectedTransactionId={selectedTransactionId} />

                {/* Кнопка для скачивания шаблона */}
                <DownloadTemplateButton />

                {/* Кнопка для загрузки изображения */}
                <UploadImageButton onFileUpload={handleFileUpload} />

                {/* Кнопка "Продолжить" */}
                <ContinueButton selectedTransactionId={selectedTransactionId} fileName={selectedFile?.name} />

                <button className="button_withe" onClick={handleBackClick}>
                    <strong>Назад</strong>
                </button>
            </div>

        </div>
    );
}