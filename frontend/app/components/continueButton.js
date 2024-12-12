'use client';

import { useRouter } from 'next/navigation';

export default function ContinueButton({ selectedTransaction, files }) {
  const router = useRouter();

  // Проверяем, загружены ли все обязательные файлы
  const isSubmitDisabled = !files.template || !files.document1;

  const handleSubmit = async () => {
    if (isSubmitDisabled) {
      alert('Пожалуйста, загрузите все обязательные документы.');
      return;
    }

    const applicationData = {
      id: new Date().getTime(), // Генерация уникального ID
      transactionId: selectedTransaction.id,
      submissionDate: new Date().toISOString(),
      category: selectedTransaction.category,
      amount: selectedTransaction.amount,
      status: 'Отправлено',
      transactionDate: selectedTransaction.date,
      mccCode: selectedTransaction.mcc_code,
      description: selectedTransaction.description,
      files: {
        template: files.template.name,
        document1: files.document1.name,
        document2: files.document2?.name || null,
        document3: files.document3?.name || null,
      },
    };

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

      router.push('/pages/submission-confirmation');
    } catch (error) {
      console.error('Ошибка:', error);
    }
  };

  return (
    <button
      className={`button_up ${isSubmitDisabled ? 'button_disabled' : 'button_upf'}`}
      onClick={handleSubmit}
      disabled={isSubmitDisabled}
    >
      Отправить заявление
    </button>
  );
}
