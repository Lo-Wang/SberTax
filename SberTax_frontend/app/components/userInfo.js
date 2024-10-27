'use client';

// Импортируем компонент для работы с изображениями
import Image from 'next/image';
import logo from '../img/logo.png';

export default function UserInfo() {
    // Пример данных пользователя (заменить на реальные данные)
    const userData = {
        lastName: 'Иванов',
        firstName: 'Иван',
        logo: '/img/logo.png',
    };

    return (
        <div className="userInfoContainer">
            <div className="circle">
                <Image src={userData.logo} alt="logo" width={100} height={100} />
            </div>
            <h2>{`${userData.lastName} ${userData.firstName}`}</h2>
        </div>
    );
}