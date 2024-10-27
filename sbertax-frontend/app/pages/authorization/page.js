'use client';

import PhoneButton from '@/app/components/phoneButton';
import SberIDButton from '@/app/components/sberIDButton';
import Image from 'next/image';
import logo from './img/logo.png';

export default function Authorization() {
    return (
        <div className="container">
            <h1 className="title">SberTax</h1>
            <div className="circle">
                <Image src={logo} alt="SberTax Logo" width={100} height={100} />
            </div>
            <p className="subtitle">Выберите способ входа</p>

            <PhoneButton />

            <SberIDButton />

            <div className="checkboxContainer">
                <input type="checkbox" id="agreement" />
                <label htmlFor="agreement" className="label">Соглашение на обработку</label>
            </div>
        </div>
    );
}