'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';

export default function SberIDButton() {
    const router = useRouter(); // Создаем экземпляр роутера

    const handleSberIDClick = () => {
        console.log('SberID clicked');
        router.push('/pages/dashboard');
    };

    return (
        <button className="button_gr" onClick={handleSberIDClick}>
            По SberID
        </button>
    );
}