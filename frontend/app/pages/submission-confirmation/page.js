'use client';

import { useRouter } from 'next/navigation';
import './styles.css';

export default function SubmissionConfirmation() {
  const router = useRouter();

  const handleBackToHome = () => {
    router.push('/pages/dashboard'); // Переход на главную страницу
  };

  return (
    <div className="containerBox">
      <div className="confirmationBox">
        <h1 className="titleB">Заявка отправлена!</h1>
        <p className="message">
          Ваши файлы успешно загружены<br />и отправлены на проверку.
        </p>
        <button className="button" onClick={handleBackToHome}>
          На главную
        </button>
      </div>
    </div>
  );
}
