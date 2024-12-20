import axios from 'axios';

const axiosInstance = axios.create({
  baseURL: 'http://94.51.125.211:8000/', // Укажите базовый URL для API
  headers: {
    'Content-Type': 'application/json',
  },
});

export default axiosInstance;