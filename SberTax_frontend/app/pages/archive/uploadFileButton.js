'use client';

import { useRef, useState } from 'react';
import styles from './uploadFileButton.module.css';

export default function UploadFileButton({ label, onFileUpload }) {
  const fileInputRef = useRef(null);
  const [uploading, setUploading] = useState(false);
  const [uploadedFileName, setUploadedFileName] = useState('');
  const [uploadSuccess, setUploadSuccess] = useState(false);
  const [errorMessage, setErrorMessage] = useState('');

  const MAX_FILE_SIZE_MB = 10; // Максимальный размер файла в МБ
  const VALID_EXTENSIONS = ['pdf', 'png', 'jpg', 'jpeg']; // Допустимые форматы
  const MAX_FILENAME_LENGTH = 20; // Максимальная длина имени файла для отображения

  const truncateFileName = (name) => {
    if (name.length > MAX_FILENAME_LENGTH) {
      const extIndex = name.lastIndexOf('.'); // Найти точку перед расширением
      const extension = name.slice(extIndex); // Получить расширение файла
      const truncated = name.slice(0, MAX_FILENAME_LENGTH - extension.length - 3); // Обрезать имя файла
      return `${truncated}...${extension}`; // Вернуть сокращённое имя
    }
    return name;
  };

  const handleButtonClick = () => {
    fileInputRef.current.click();
  };

  const handleFileChange = (event) => {
    const file = event.target.files[0];

    if (!file) return;

    const fileExtension = file.name.split('.').pop().toLowerCase();

    // Проверка формата
    if (!VALID_EXTENSIONS.includes(fileExtension)) {
      setErrorMessage('Ошибка: допустимые форматы - PDF, PNG, JPG, JPEG.');
      return;
    }

    // Проверка размера
    if (file.size / 1024 / 1024 > MAX_FILE_SIZE_MB) {
      setErrorMessage(`Ошибка: файл не должен превышать ${MAX_FILE_SIZE_MB} МБ.`);
      return;
    }

    setUploading(true);
    setErrorMessage('');

    // Имитируем успешную загрузку
    setTimeout(() => {
      setUploading(false);
      setUploadedFileName(file.name);
      onFileUpload(file);
    }, 1000);
  };

  return (
    <div className={styles.uploadContainer}>
      <input
        type="file"
        ref={fileInputRef}
        accept=".pdf,.png,.jpg,.jpeg"
        onChange={handleFileChange}
        style={{ display: 'none' }}
        id="file-upload"
      />
      <label className={`${styles.fileUploadLabel} ${uploading ? styles.uploading : ''}`}>
        <button
          className={`button_file ${uploadedFileName ? 'button_file_white' : 'button_file'}`}
          onClick={handleButtonClick}
          disabled={uploading}
        >
          {uploading
            ? 'Загрузка...'
            : uploadedFileName
              ? truncateFileName(uploadedFileName)
              : label}
        </button>
      </label>
      <p className={styles.fileTypesInfo}>
        Файлы: PDF, PNG, JPG, JPEG до 10 МБ.
      </p>
      {errorMessage && <p className={styles.errorMessage}>{errorMessage}</p>}
    </div>
  );
}
