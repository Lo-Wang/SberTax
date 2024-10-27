import { useRef } from 'react';

export default function UploadImageButton({ onFileUpload }) {
  const fileInputRef = useRef(null);

  const handleButtonClick = () => {
    fileInputRef.current.click(); // Открываем диалоговое окно для выбора файла
  };

  const handleFileChange = (event) => {
    const file = event.target.files[0];
    onFileUpload(file); // Передаем файл в родительский компонент
  };

  return (
    <div className="uploadContainer">
      <button className="button_upload" onClick={handleButtonClick}>
        Загрузить изображение
      </button>
      <input
        type="file"
        ref={fileInputRef}
        style={{ display: 'none' }}
        onChange={handleFileChange}
      />
    </div>
  );
}
