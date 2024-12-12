'use client';

import Image from 'next/image';
import styles from './userInfo.module.css'; // Подключаем стили
import ProgressBar from './progressBar';

export default function UserInfo() {
    const userData = {
        lastName: 'Иванов',
        firstName: 'Иван',
        logo: '/img/logo.png',
        coins: 1000,
        maxCoins: 15600,
    };

    return (
        <div className={styles.userInfoContainer}>
            <div className={styles.circle}>
                <Image src={userData.logo} alt="logo" width={100} height={100} />
            </div>
            <h2 className={styles.userName}>{`${userData.firstName}`}</h2>
            <ProgressBar coins={userData.coins} maxCoins={userData.maxCoins} />
        </div>
    );
}
