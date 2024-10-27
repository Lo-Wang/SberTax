'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';

export default function StatusPage() {
  const [applications, setApplications] = useState([]);

  useEffect(() => {
    const fetchApplications = async () => {
      try {
        const response = await fetch('/api/getApplications'); // Предполагаем, что есть API для получения заявок
        if (!response.ok) {
          throw new Error('Ошибка при получении заявок');
        }
        const data = await response.json();
        setApplications(data);
      } catch (error) {
        console.error(error);
      }
    };

    fetchApplications();
  }, []);

  return (
    <div className="container">
      <h1 className="title">Статус Заявки</h1>
      <div className="scrollArea">
        {applications.length > 0 ? (
          applications.map((app, index) => (
            <div key={index} className="applicationCard">
              <p><strong>ID Заявки:</strong> {app.id}</p>
              <p><strong>Статус:</strong> {app.status}</p>
              <p><strong>Имя файла:</strong> {app.fileName}</p>
              <p>Дата: {new Date(app.date).toLocaleString()}</p>
            </div>
          ))
        ) : (
          <p>Нет поданных заявок.</p>
        )}
      </div>
      <Link href="/pages/dashboard">
        <button className="button_withe">Назад</button>
      </Link>
    </div>
  );
}
