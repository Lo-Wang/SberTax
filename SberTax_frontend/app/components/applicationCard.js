'use client';

import { useRouter } from 'next/navigation';
import './applicationCard.module.css';

export default function ApplicationCard({ application }) {
  const router = useRouter();

  const getStatusClass = (status) => {
    switch (status.toLowerCase()) {
      case 'принято':
        return 'accepted';
      case 'отклонено':
        return 'rejected';
      case 'отправлено':
        return 'sent';
      case 'редактирование':
        return 'editing';
      default:
        return '';
    }
  };

  const handleCardClick = () => {
    router.push(`/pages/application/${application.id}`); // Навигация на страницу заявки
  };

  return (
    <div className="applicationCard" onClick={handleCardClick}>
      <div className="applicationDate">
        {new Date(application.submissionDate).toLocaleDateString()}
      </div>
      <div className="applicationDetails">№ заявки: {application.id}</div>
      <div className="applicationDetails">{application.category}</div>
      <div className={`applicationStatus ${getStatusClass(application.status)}`}>
        {application.status}
      </div>
    </div>
  );
}
