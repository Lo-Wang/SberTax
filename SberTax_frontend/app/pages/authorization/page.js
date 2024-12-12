'use client';

import { useState } from 'react';
import axiosInstance from '/utils/axiosInstance';
import './styles.css';

export default function AuthorizationPage() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const handleLogin = async () => {
    try {
      const response = await axiosInstance.post('/auth/token', {
        username,
        password,
      });
      console.log('Токен:', response.data.access_token);
      localStorage.setItem('token', response.data.access_token); // Сохраняем токен
      alert('Успешный вход!');
    } catch (err) {
      console.error('Ошибка авторизации:', err);
      setError('Неверные учетные данные.');
    }
  };

  return (
    <div className="container">
      <h1 className="title">Вход</h1>
      <div className="form-group">
        <input
          type="text"
          placeholder="Имя пользователя"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />
        <input
          type="password"
          placeholder="Пароль"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        {error && <p className="error-message">{error}</p>}
        <button className="button" onClick={handleLogin}>
          Войти
        </button>
      </div>
    </div>
  );
}
