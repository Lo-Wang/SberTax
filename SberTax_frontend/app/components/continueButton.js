"use client";

import { useRouter } from 'next/navigation';

export default function ContinueButton({ selectedTransactionId, fileName }) {
  const router = useRouter();

  const handleSubmit = async () => {
    console.log("Selected Transaction ID:", selectedTransactionId);
    console.log("File Name:", fileName);

    if (!selectedTransactionId) {
      alert("Пожалуйста, выберите транзакцию.");
      return;
    }

    if (!fileName) {
      alert("Пожалуйста, загрузите изображение.");
      return;
    }

    // Создаем объект заявки
    const applicationData = {
      id: new Date().getTime(), // Пример ID на основе времени
      transactionId: selectedTransactionId,
      fileName: fileName,
      status: 'Отправлен', // Пример статуса
    };

    // Сохраняем данные заявки в файл applications.json
    try {
      const response = await fetch('/api/saveApplication', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(applicationData),
      });
  
      if (!response.ok) {
        throw new Error('Ошибка при отправке заявки');
      }
  
      const data = await response.json();
      console.log(data.message);
      router.push('/pages/dashboard'); // Перенаправление после успешной отправки
    } catch (error) {
      console.error('Ошибка:', error);
    }
  };

  return (
    <button className="button_gr" onClick={handleSubmit}>
      Продолжить
    </button>
  );
}
