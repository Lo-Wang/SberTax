'use client';

import { useState, useEffect } from 'react';
import UploadFileButton from '@/app/components/uploadFileButton';
import ContinueButton from '@/app/components/continueButton'; // Импортируем кнопку ContinueButton
import { useRouter } from 'next/navigation';
import './styles.css';

export default function UploadDocumentsPage({ params }) {
  const { id } = params; // ID заявки из URL
  const [files, setFiles] = useState({
    template: null,
    requisites: null,
  });
  const [selectedTransaction, setSelectedTransaction] = useState(null);
  const router = useRouter();

  useEffect(() => {
    // Загружаем данные транзакции из JSON
    const fetchTransaction = async () => {
      try {
        const response = await fetch('/transactions/file.json'); // Предполагаем, что файл транзакций доступен здесь
        if (!response.ok) {
          throw new Error('Ошибка при загрузке транзакции');
        }
        const data = await response.json();
        const transaction = data.find((item) => item.id.toString() === id);
        setSelectedTransaction(transaction);
      } catch (error) {
        console.error('Ошибка загрузки транзакции:', error);
      }
    };

    fetchTransaction();
  }, [id]);

  const handleFileUpload = (key, file) => {
    setFiles((prev) => ({
      ...prev,
      [key]: file,
    }));
  };

  if (!selectedTransaction) {
    return (
      <div className="container">
        <p>Загрузка данных транзакции...</p>
      </div>
    );
  }

  return (
    <div className="container">
      <h1 className="title">
        Загрузите документы <br />
        для заявки
      </h1>
      <div className="file-upload-section">
        <div className="file-upload-block">
          <p className="file-upload-title">Заполненный шаблон заявления (обязательно)</p>
          <UploadFileButton
            label={files.template ? files.template.name : 'Загрузите файл'}
            onFileUpload={(file) => handleFileUpload('template', file)}
          />
        </div>
        <div className="file-upload-block">
          <p className="file-upload-title">Справка</p>
          <UploadFileButton
            label={files.requisites ? files.requisites.name : 'Загрузите файл'}
            onFileUpload={(file) => handleFileUpload('requisites', file)}
          />
        </div>
      </div>
      <div className="button-container">
        {/* Кнопка ContinueButton */}
        <ContinueButton selectedTransaction={selectedTransaction} files={files} />
        <button
          className="button_back"
          onClick={() => router.push('/pages/submit-application')}
        >
          Назад
        </button>
      </div>
    </div>
  );
}