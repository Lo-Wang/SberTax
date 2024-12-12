'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import './styles.css';

export default function ApplicationDetailsPage({ params }) {
  const { id } = params; // Получаем ID из URL
  const [application, setApplication] = useState(null);
  const [showConfirmDelete, setShowConfirmDelete] = useState(false); // Состояние для отображения окна подтверждения удаления
  const router = useRouter();

  useEffect(() => {
    const fetchApplication = async () => {
      try {
        const response = await fetch('/api/getApplications');
        if (!response.ok) {
          throw new Error('Ошибка при загрузке заявки');
        }
        const data = await response.json();
        const app = data.find((item) => item.id.toString() === id);
        setApplication(app || null);
      } catch (error) {
        console.error('Ошибка загрузки данных:', error);
      }
    };

    fetchApplication();
  }, [id]);

  const getStatusStyle = (status) => {
    switch (status.toLowerCase()) {
      case 'принято':
        return 'status-accepted';
      case 'отклонено':
        return 'status-rejected';
      case 'отправлено':
        return 'status-sent';
      case 'редактирование':
        return 'status-editing';
      default:
        return '';
    }
  };

  const handleDeleteClick = async () => {
    try {
      const response = await fetch(`/api/deleteApplication/${id}`, {
        method: 'DELETE',
      });
      if (!response.ok) {
        throw new Error('Ошибка при удалении заявки');
      }
      alert('Заявка успешно удалена');
      router.push('/pages/status');
    } catch (error) {
      console.error('Ошибка удаления заявки:', error);
      alert('Не удалось удалить заявку');
    }
  };

  const handleEditClick = () => {
    router.push(`/pages/application/edit-application/${id}`);
  };

  if (!application) {
    return (
      <div className="container">
        <div className="button-container">
          <p className='pCenter'>Заявка не найдена.</p>
          <button className="button_back" onClick={() => router.push('/pages/status')}>
            Назад
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="application-details-container">
      <div className={`application-status ${getStatusStyle(application.status)}`}>
        {application.status}
      </div>
      <h3 className="application-id">№ заявки: {application.id}</h3>
      <div className="application-details">
        <div className="details-row">
          <span>Дата подачи:</span>
          <span>
            {new Date(application.submissionDate).toLocaleDateString('ru-RU', {
              year: 'numeric',
              month: 'long',
              day: 'numeric',
            })}
          </span>
        </div>
        <hr className="divider" />
        <div className="details-row">
          <span>Категория:</span>
          <span>{application.category}</span>
        </div>
        <hr className="divider" />
        <div className="details-row">
          <span>Сумма:</span>
          <span>{application.amount.toLocaleString('ru-RU')} руб.</span>
        </div>
        <hr className="divider" />
        <div className="details-row">
          <span>Описание:</span>
          <span>{application.description}</span>
        </div>
        <hr className="divider" />
        <div className="details-row">
          <span>Дата транзакции:</span>
          <span>
            {new Date(application.transactionDate).toLocaleDateString('ru-RU', {
              year: 'numeric',
              month: 'long',
              day: 'numeric',
            })}
          </span>
        </div>
      </div>
      <div className="button-container">
        {application.status.toLowerCase() === 'отправлено' && (
          <button className="button_delete" onClick={() => setShowConfirmDelete(true)}>
            Удалить
          </button>
        )}
        {application.status.toLowerCase() === 'редактирование' && (
          <button className="button_edit" onClick={handleEditClick}>
            Редактировать
          </button>
        )}
        <button className="button_back" onClick={() => router.push('/pages/status')}>
          Назад
        </button>
      </div>

      {showConfirmDelete && (
        <>
          <div className="confirm-delete-overlay" onClick={() => setShowConfirmDelete(false)}></div>
          <div className="confirm-delete-popup">
            <p>Вы уверены, что хотите удалить эту заявку?</p>
            <div className='button-container'>
              <button className="button_delete" onClick={handleDeleteClick}>
                Удалить
              </button>
              <button className="button_back" onClick={() => setShowConfirmDelete(false)}>
                Отмена
              </button>
            </div>
          </div>
        </>
      )}
    </div>
  );
}
