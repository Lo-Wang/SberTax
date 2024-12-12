'use client';

import UserInfo from '@/app/components/userInfo'; // Компонент для информации пользователя
import { useRouter } from 'next/navigation'; // Импортируем useRouter для навигации
import './styles.css'; // Подключаем стили

export default function Dashboard() {
  const router = useRouter(); // Создаем экземпляр роутера

  const handleStatusClick = () => {
    router.push('/pages/status'); // Переход к странице статуса заявки
  };

  const handleTransactionsClick = () => {
    router.push('/pages/transaction'); // Переход к странице подходящих транзакций
  };

  const handleSubmitApplicationClick = () => {
    router.push('/pages/submit-application'); // Переход к странице подачи заявки
  };

  const handleBackClick = () => {
    router.push('/pages/authorization'); // Возврат к авторизации
  };

  return (
    <div className="container">
      <UserInfo />
      <div className="button-container">
        <button className="button" onClick={handleStatusClick}>
          Статус заявки
        </button>
        <button className="button" onClick={handleTransactionsClick}>
          Подходящие транзакции
        </button>
        <button className="button" onClick={handleSubmitApplicationClick}>
          Подать заявку
        </button>
        <button className="button_back" onClick={handleBackClick}>
          Выйти
        </button>
      </div>
    </div>
  );
}
