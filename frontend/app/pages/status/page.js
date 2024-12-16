'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';
import ApplicationCard from '@/app/components/applicationCard';
import axiosInstance from '/utils/axiosInstance';
import './styles.css';

export default function StatusPage() {
  const [applications, setApplications] = useState([]);

  useEffect(() => {
    const fetchApplications = async () => {
      try {
        const response = await axiosInstance.get('/transactions/?skip=0&limit=10', {
          headers: {
            accept: 'application/json',
          },
        });

        const sortedApplications = response.data.sort(
          (a, b) => new Date(b.created_at) - new Date(a.created_at) // Сортируем по created_at
        );
        setApplications(sortedApplications);
      } catch (error) {
        console.error('Ошибка при получении заявок:', error);
      }
    };

    fetchApplications();
  }, []);

  return (
    <div className="container">
      <h1 className="title">Статусы заявок</h1>
      <div className="scrollAreaStatus">
        {applications.length > 0 ? (
          applications.map((app) => <ApplicationCard key={app.id} application={app} />)
        ) : (
          <p>Нет поданных заявок.</p>
        )}
      </div>
      <div className="button-container">
        <Link href="/pages/dashboard">
          <button className="button_back">Назад</button>
        </Link>
      </div>
    </div>
  );
}