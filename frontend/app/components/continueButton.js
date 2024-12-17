'use client';

import { useRouter } from 'next/navigation';
import axiosInstance from '/utils/axiosInstance'; // Убедитесь, что путь к axiosInstance правильный

export default function ContinueButton({ selectedTransaction, files }) {
  const router = useRouter();

  const handleSubmit = async () => {
    const formData = new FormData();

    // Добавляем данные транзакции в FormData
    formData.append('amount', selectedTransaction.amount);
    formData.append('category', selectedTransaction.category);
    formData.append('mcc_code', selectedTransaction.mcc_code);
    formData.append('description', selectedTransaction.description);

    // Добавляем user_id из localStorage
    const userId = localStorage.getItem('user_id');
    if (userId) {
      formData.append('user_id', userId); // Добавляем user_id в FormData
    }

    // Добавляем файл в FormData, если он существует
    if (files.template) {
      formData.append('file', files.template); // Предполагается, что files.template - это объект File
    }

    try {
      const response = await axiosInstance.post('/documents/downloads', formData, {
        headers: {
          'Content-Type': 'multipart/form-data', // Убедитесь, что заголовок установлен правильно
        },
      });

      console.log(response.data.message); // Предполагается, что ответ содержит поле message

      router.push('/pages/submission-confirmation');
    } catch (error) {
      console.error('Ошибка:', error);
      // Вы можете добавить обработку ошибок, чтобы показать пользователю сообщение об ошибке
    }
  };

  return (
    <button
      className="button_up button_upf"
      onClick={handleSubmit}
    >
      Отправить заявление
    </button>
  );
}