'use client';

import { useRef, useState } from 'react';
import styles from './uploadFileButton.module.css';

export default function UploadFileButton({ onFileUpload }) {
  const fileInputRef = useRef(null);
  const [uploading, setUploading] = useState(false);
  const [uploadSuccess, setUploadSuccess] = useState(false);
  const [errorMessage, setErrorMessage] = useState('');

  const handleFileChange = async (event) => {
    const file = event.target.files[0];

    console.log('Загружаемый файл:', file);

    if (!file) return;

    const validExtensions = ['pdf', 'png', 'jpg', 'jpeg'];
    const fileExtension = file.name.split('.').pop().toLowerCase();

    if (!validExtensions.includes(fileExtension)) {
      setErrorMessage('Ошибка: допустимые форматы файлов - PDF, PNG, JPG, JPEG.');
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

      onFileUpload(file); // Передаём файл в родительский компонент
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
      <label
        htmlFor="file-upload"
        className={`${styles['file-upload-label']} ${uploading ? styles.uploading : ''} ${
          uploadSuccess ? styles.success : ''
        }`}
      >
        {uploading ? 'Загрузка...' : uploadSuccess ? 'Заменить файл' : 'Загрузить файл'}
      </label>
      <p className={styles['file-types-info']}>Форматы: PDF, PNG, JPG, JPEG</p>
      {uploading && <div className={styles['loading-bar']}></div>}
      {errorMessage && <p className={styles['error-message']}>{errorMessage}</p>}
    </div>
  );
}
