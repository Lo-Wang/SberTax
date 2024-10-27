'use client';

import PhoneButton from '@/app/components/phoneButton';
import SberIDButton from '@/app/components/sberIDButton';
import styles from '../styles/Authorization.module.css';
import Image from 'next/image';
import logo from '../img/logo.png';

export default function Authorization() {
    return (
        <div className={styles.container}>
            <h1 className={styles.title}>SberTax</h1>
            <div className={styles.circle}>
                <Image src={logo} alt="SberTax Logo" width={100} height={100} />
            </div>
            <p className={styles.subtitle}>Выберите способ входа</p>

            <PhoneButton />

            <SberIDButton/>

            <div className={styles.checkboxContainer}>
                <input type="checkbox" id="agreement" />
                <label htmlFor="agreement" className={styles.label}>Соглашение на обработку</label>
            </div>
        </div>
    );
}