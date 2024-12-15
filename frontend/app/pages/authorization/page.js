'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import axiosInstance from '/utils/axiosInstance';
import './styles.css';

export default function AuthorizationPage() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [email, setEmail] = useState('');
  const [isRegistering, setIsRegistering] = useState(false);
  const [error, setError] = useState('');
  const [successMessage, setSuccessMessage] = useState('');
  const router = useRouter();

  const handleLogin = async () => {
    try {
      const formData = new URLSearchParams();
      formData.append('username', username);
      formData.append('password', password);

      const response = await axiosInstance.post('/login', formData, {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
      });

      console.log('Токен:', response.data.access_token);
      localStorage.setItem('token', response.data.access_token);
      router.push('/pages/dashboard');
    } catch (err) {
      console.error('Ошибка авторизации:', err);
      setError('Неверные учетные данные.');
    }
  };

  const handleRegister = async () => {
    try {
      const response = await axiosInstance.post('/registry', {
        username,
        password,
        email,
      });

      setSuccessMessage('Регистрация успешна! Теперь вы можете войти.');
      setIsRegistering(false);
      setUsername('');
      setPassword('');
      setEmail('');
    } catch (err) {
      console.error('Ошибка регистрации:', err);
      setError('Не удалось зарегистрироваться. Проверьте данные.');
    }
  };

  return (
    <div className="container">
      <h1 className="title">{isRegistering ? 'Регистрация' : 'Вход'}</h1>
      <div className="form-group">
        <input
          type="text"
          placeholder="Имя пользователя"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />
        {isRegistering && (
          <input
            type="email"
            placeholder="Электронная почта"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
        )}
        <input
          type="password"
          placeholder="Пароль"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        {error && <p className="error-message">{error}</p>}
        {successMessage && <p className="success-message">{successMessage}</p>}
      </div>
      <div className='button-container'>
        <button
          className="button"
          onClick={isRegistering ? handleRegister : handleLogin}
        >
          {isRegistering ? 'Зарегистрироваться' : 'Войти'}
        </button>
        <p
          className="button_white"
          onClick={() => {
            setIsRegistering(!isRegistering);
            setError('');
            setSuccessMessage('');
          }}
        >
          {isRegistering ? 'Войти' : 'Зарегистрироваться'}
        </p>
      </div>
    </div>
  );
}