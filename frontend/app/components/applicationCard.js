'use client';

import { useRouter } from 'next/navigation';
import './applicationCard.module.css';

export default function ApplicationCard({ application }) {
  const router = useRouter();

  const handleCardClick = () => {
    router.push(`/pages/application/${application.id}`); // Навигация на страницу заявки
  };

  return (
    <div className="applicationCard" onClick={handleCardClick}>
      <div className="applicationDate">
        {new Date(application.created_at).toLocaleDateString()} {/* Используем created_at */}
      </div>
      <div className="applicationDetails">№ заявки: {application.id}</div>
      <div className="applicationDetails">{application.category}</div>
      <div className="applicationDetails">Сумма: {application.amount} руб.</div> {/* Добавляем сумму */}
      <div className="applicationDetails">MCC код: {application.mcc_code}</div> {/* Добавляем MCC код */}
      <div className="applicationDetails">Описание: {application.description}</div> {/* Добавляем описание */}
    </div>
  );
}