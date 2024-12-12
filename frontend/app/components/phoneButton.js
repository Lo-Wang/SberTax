'use client';

import { useRouter } from 'next/navigation';

export default function PhoneButton() {
  const router = useRouter();

  return (
    <button
      className="button"
      onClick={() => router.push('/pages/dashboard')}
    >
      Войти по номеру телефона
    </button>
  );
}
