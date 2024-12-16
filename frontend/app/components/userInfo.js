'use client';

import { useEffect, useState } from 'react';
import Image from 'next/image';
import styles from './userInfo.module.css'; // Подключаем стили
import ProgressBar from './progressBar';
import axiosInstance from '/utils/axiosInstance'; // Импортируйте ваш axiosInstance

export default function UserInfo() {
    const [userData, setUser ] = useState({
        logo: '/img/logo.png', // Фиксированное значение
        coins: 1000,          // Фиксированное значение
        maxCoins: 15600,      // Фиксированное значение
        first_name: '',       // Поля, которые будут обновлены из API
        last_name: '',
    });
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');
    const [currentUsername, setCurrentUsername] = useState(null); // Состояние для username

    useEffect(() => {
        // Получаем username из localStorage только на клиенте
        const username = localStorage.getItem('username');
        setCurrentUsername(username);
    }, []); // Пустой массив зависимостей, чтобы выполнить только один раз при монтировании

    useEffect(() => {
        const fetchUserData = async () => {
            if (!currentUsername) {
                setError('Пользователь не авторизован.');
                setLoading(false);
                return;
            }
            try {
                const response = await axiosInstance.get(`/auth/users/me?username=${currentUsername}`, {
                    headers: {
                        'accept': 'application/json' // Устанавливаем заголовок accept
                    }
                }); // Запрос к вашему эндпоинту с username
                setUser (prevData => ({
                    ...prevData,
                    first_name: response.data.first_name,
                    last_name: response.data.last_name,
                }));
            } catch (err) {
                console.error('Ошибка при получении данных пользователя:', err);
                setError('Не удалось загрузить данные пользователя.');
            } finally {
                setLoading(false);
            }
        };

        if (currentUsername) {
            fetchUserData();
        }
    }, [currentUsername]); // Добавляем currentUsername в зависимости

    if (loading) {
        return <p>Загрузка...</p>;
    }

    if (error) {
        return <p>{error}</p>;
    }

    return (
        <div className={styles.userInfoContainer}>
            <div className={styles.circle}>
                <Image src={userData.logo} alt="logo" width={100} height={100} />
            </div>
            <h2 className={styles.userName}>{`${userData.first_name} ${userData.last_name}`}</h2>
            <ProgressBar coins={userData.coins} maxCoins={userData.maxCoins} />
        </div>
    );
}