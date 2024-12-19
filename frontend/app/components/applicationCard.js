'use client';

import { useRouter } from 'next/navigation';
import './applicationCard.module.css';

export default function ApplicationCard({ application }) {
  const router = useRouter();

  return (
    <div className="applicationCard">
      <div className="applicationDate">
        {new Date(application.created_at).toLocaleDateString()} {/* Используем created_at */}
      </div>
      {/* <div className="applicationDetails">№ заявки: {application.id}</div> */}
      <div className="applicationDetails">{application.category}</div>
      <div className="applicationDetails">Сумма: {application.amount} руб.</div> {/* Добавляем сумму */}
      {/*<div className="applicationDetails">MCC код: {application.mcc_code}</div>*/} {/* Добавляем MCC код */}
      <div className="applicationDetails">Описание: {application.description}</div> {/* Добавляем описание */}
      <div className="applicationStatus accepted">Статус: Выполнено</div> {/* Статус выполнен */}
    </div>
  );
}