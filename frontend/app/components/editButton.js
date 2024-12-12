'use client';

import { useRouter } from 'next/navigation';

export default function EditButton({ id, files }) {
  const router = useRouter();

  const handleSubmit = async () => {
    if (!files.template || !files.document1) {
      alert('Пожалуйста, загрузите обязательные документы.');
      return;
    }

    const updatedData = {
      id,
      files: {
        template: files.template.name,
        document1: files.document1.name,
        document2: files.document2?.name || '',
        document3: files.document3?.name || '',
      },
    };

    try {
      const response = await fetch('/api/editApplication', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(updatedData),
      });

      if (!response.ok) {
        throw new Error('Ошибка при редактировании заявки');
      }

      router.push('/pages/application/edit-application/edit-confirmation'); // Перенаправление на страницу подтверждения
    } catch (error) {
      console.error('Ошибка:', error);
    }
  };

  return (
    <button
      className="button"
      onClick={handleSubmit}
      disabled={!files.template || !files.document1}
    >
      Редактировать данные
    </button>
  );
}
