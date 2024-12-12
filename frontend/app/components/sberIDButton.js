'use client';

import { useRouter } from 'next/navigation';

export default function SberIDButton() {
  const router = useRouter();

  return (
    <button className="button" onClick={() => router.push('/pages/dashboard')}>
      По SberID
    </button>
  );
}
