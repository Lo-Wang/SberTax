'use client';

import PhoneButton from '@/app/components/phoneButton';
import SberIDButton from '@/app/components/sberIDButton';
import CheckboxWithLabel from '@/app/components/CheckboxWithLabel';
import Image from 'next/image';
import logo from '@/app/img/logo.png';
import './styles.css';

export default function AuthorizationPage() {
  return (
    <div className="container">
      <h1 className="auth-title">SberTax</h1>
      <div className="auth-logo">
        <Image src={logo} alt="SberTax Logo" width={120} height={120} />
      </div>
      <div className="button-container">
        <SberIDButton />
        <PhoneButton />
      </div>
      <CheckboxWithLabel
        id="agreementCheckbox"
        label="Соглашение на обработку данных"
        onChange={(e) => console.log(e.target.checked)}
      />
    </div>
  );
}
