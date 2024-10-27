'use client';

import UserInfo from '@/app/components/userInfo'; // Импортируем компонент для информации пользователя
import { useRouter } from 'next/navigation'; // Импортируем useRouter для навигации

export default function Dashboard() {
  const router = useRouter(); // Создаем экземпляр роутера

  const handleStatusClick = () => {
    router.push('/pages/status'); // Путь к странице статуса заявки
  };

  const handleTransactionsClick = () => {
    console.log('Подходящие транзакции');
    router.push('/pages/submit-application'); // Путь к странице подачи заявки
  };

  const handleSubmitApplicationClick = () => {
    router.push('/pages/submit-application'); // Путь к странице подачи заявки
  };

  const handleBackClick = () => {
    router.push('/'); // Путь к странице подачи заявки
  };

  return (
    <div className="container">
      <UserInfo />
      <div className="buttonContainer">
        <button className="button_gr" onClick={handleStatusClick}>
          Статус заявки
        </button>
        <button className="button_gr" onClick={handleTransactionsClick}>
          Подходящие транзакции
        </button>
        <button className="button_gr" onClick={handleSubmitApplicationClick}>
          Подать заявку
        </button>
        <button className="button_withe" onClick={handleBackClick}>
          <strong>Выход</strong>
        </button>
      </div>
    </div>
  );
}