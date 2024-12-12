'use client';

import { useRef, useState, useEffect } from 'react';
import styles from './uploadFileButton.module.css';

export default function UploadFileButton({ label, onFileUpload }) {
  const fileInputRef = useRef(null);
  const [uploading, setUploading] = useState(false);
  const [fileName, setFileName] = useState(label || 'Загрузите файл');
  const [errorMessage, setErrorMessage] = useState('');

  const MAX_FILE_SIZE_MB = 10;
  const VALID_EXTENSIONS = ['pdf', 'png', 'jpg', 'jpeg'];
  const MAX_FILE_NAME_LENGTH = 20; // Максимальная длина имени файла

  const truncateFileName = (name) => {
    if (name.length > MAX_FILE_NAME_LENGTH) {
      return `${name.substring(0, MAX_FILE_NAME_LENGTH)}...`;
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
    if (!VALID_EXTENSIONS.includes(fileExtension)) {
      setErrorMessage('Ошибка: допустимые форматы - PDF, PNG, JPG, JPEG.');
      return;
    }

    if (file.size / 1024 / 1024 > MAX_FILE_SIZE_MB) {
      setErrorMessage(`Ошибка: файл не должен превышать ${MAX_FILE_SIZE_MB} МБ.`);
      return;
    }

    setUploading(true);
    setErrorMessage('');

    setTimeout(() => {
      setFileName(truncateFileName(file.name));
      onFileUpload(file);
      setUploading(false);
    }, 1000);
  };

  useEffect(() => {
    if (label) {
      setFileName(truncateFileName(label)); // Устанавливаем имя файла из переданных данных
    }
  }, [label]);

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
        className={`button_file`}
        onClick={handleButtonClick}
        disabled={uploading}
      >
        {uploading ? 'Загрузка...' : fileName}
      </button>
      <p className={styles.fileTypesInfo}>
        Допустимые форматы: PDF, PNG, JPG, JPEG до 10 МБ.
      </p>
      {errorMessage && <p className={styles.errorMessage}>{errorMessage}</p>}
    </div>
  );
}
