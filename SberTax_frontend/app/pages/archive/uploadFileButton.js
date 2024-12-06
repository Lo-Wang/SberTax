'use client';

import { useRef, useState } from 'react';
import styles from './uploadFileButton.module.css';

export default function UploadFileButton({ onFileUpload }) {
  const fileInputRef = useRef(null);
  const [uploading, setUploading] = useState(false);
  const [uploadSuccess, setUploadSuccess] = useState(false);
  const [errorMessage, setErrorMessage] = useState('');

  const MAX_FILE_SIZE_MB = 10; // Максимальный размер файла в МБ

  const handleButtonClick = () => {
    fileInputRef.current.click();
  };

  const handleFileChange = async (event) => {
    const file = event.target.files[0];

    if (!file) return;

    const validExtensions = ['pdf', 'png', 'jpg', 'jpeg'];
    const fileExtension = file.name.split('.').pop().toLowerCase();

    // Проверка расширения файла
    if (!validExtensions.includes(fileExtension)) {
      setErrorMessage('Ошибка: допустимые форматы файлов - PDF, PNG, JPG, JPEG.');
      return;
    }

    // Проверка размера файла
    if (file.size / 1024 / 1024 > MAX_FILE_SIZE_MB) {
      setErrorMessage(`Ошибка: размер файла не должен превышать ${MAX_FILE_SIZE_MB} МБ.`);
      return;
    }

    setUploading(true);
    setErrorMessage('');

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch('/api/uploadFile', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error('Ошибка при загрузке файла');
      }

      await response.json();
      setUploadSuccess(true);
      onFileUpload(file);
    } catch (error) {
      setErrorMessage(error.message);
    } finally {
      setUploading(false);
    }
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
      <button
        className={`button ${uploadSuccess ? 'button_white' : 'button'}`}
        onClick={handleButtonClick}
        disabled={uploading}
      >
        {uploading ? 'Загрузка...' : uploadSuccess ? 'Заменить файл' : 'Загрузить файл'}
      </button>
      <p className={styles.fileTypesInfo}>Допустимые форматы: PDF, PNG, JPG, JPEG до 10 МБ</p>
      {errorMessage && <p className={styles.errorMessage}>{errorMessage}</p>}
    </div>
  );
}
