'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';

export default function PhoneButton() {
  const [isPhoneInputVisible, setPhoneInputVisible] = useState(false);
  const [isCodeInputVisible, setCodeInputVisible] = useState(false);
  const [code, setCode] = useState(''); // Состояние для хранения кода
  const router = useRouter(); // Создаем экземпляр роутера

  const handlePhoneClick = () => {
    setPhoneInputVisible((prev) => !prev); // Переключаем состояние видимости
    setCodeInputVisible(false); // Скрываем поле для ввода кода
  };

  const handleGetCodeClick = () => {
    setCodeInputVisible(true); // Показываем поле для ввода кода
  };

  const handleConfirmCodeClick = () => {
    // Здесь можно добавить логику для подтверждения кода
    console.log('Код подтвержден:', code);
    router.push('/pages/dashboard'); // Изменяем на правильный путь к личному кабинету
  };

  return (
    <div className="phoneButtonContainer">
      <button className="button_gr" onClick={handlePhoneClick}>
        По телефону
      </button>

      {isPhoneInputVisible && (
        <div className="phoneInputContainer">
          <input type="text" placeholder="Введите номер телефона" className="input" />
          <button className="button_gr" onClick={handleGetCodeClick}>
            Получить код
          </button>
        </div>
      )}

      {isCodeInputVisible && (
        <div className="codeInputContainer">
          <input
            type="text"
            placeholder="Введите код"
            className="input"
            value={code}
            onChange={(e) => setCode(e.target.value)} // Обновляем состояние кода
          />
          <button className="button_gr" onClick={handleConfirmCodeClick}>
            Подтвердить
          </button>
        </div>
      )}
    </div>
  );
}