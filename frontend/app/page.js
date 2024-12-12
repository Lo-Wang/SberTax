'use client';

import Image from 'next/image';
import logo from './img/logo.png';
import Link from 'next/link';

export default function Authorization() {
  return (
    <div className="container">
      <div className="circle">
        <Image src={logo} alt="SberTax Logo" width={100} height={100} />
      </div>
      <div className="button-container">
        <Link href="/pages/authorization">
          <button className="button">SberTax</button>
        </Link>
      </div>
    </div>
  );
}