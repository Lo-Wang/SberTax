'use client';

import { useState } from 'react';
import TransactionList from '@/app/components/transactionList';
import DownloadTemplateButton from '@/app/components/downloadTemplateButton';
import { useRouter } from 'next/navigation';
import './styles.css';

export default function ApplicationSubmission() {
  const router = useRouter();
  const [selectedTransaction, setSelectedTransaction] = useState(null);

  const handleTransactionSelect = (transaction) => {
    console.log('Выбрана транзакция:', transaction);
    setSelectedTransaction(transaction);
  };

  const handleDownloadTemplate = () => {
    if (!selectedTransaction) {
      alert('Пожалуйста, выберите транзакцию, чтобы скачать шаблон.');
      return;
    }

    // Логика выбора шаблона по категории
    const templateCategory =
      selectedTransaction.category === 'Медицина'
        ? '/templates/medical-template.docx'
        : '/templates/education-template.docx';

    const link = document.createElement('a');
    link.href = templateCategory;
    link.download = templateCategory.split('/').pop();
    link.click();
  };

  const handleGoToUpload = () => {
    if (!selectedTransaction) {
      alert('Пожалуйста, выберите транзакцию, чтобы продолжить.');
      return;
    }

    // Переход на страницу загрузки документов с ID транзакции
    router.push(`/pages/submit-application/upload-documents/${selectedTransaction.id}`);
  };

  return (
    <div className="container">
      <h1 className="title">Выберите транзакцию</h1>
      <TransactionList onSelectTransaction={handleTransactionSelect} />
      <div className="button-container">
        <button className="button" onClick={handleDownloadTemplate}>
          Скачать шаблон
        </button>
        <button className="button" onClick={handleGoToUpload}>
          Загрузить документы
        </button>
        <button className="button_back" onClick={() => router.push('/pages/dashboard')}>
          Назад
        </button>
      </div>
    </div>
  );
}
