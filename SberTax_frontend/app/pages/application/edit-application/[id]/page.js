'use client';

import { useEffect, useState } from 'react';
import UploadFileButton from '@/app/components/uploadFileButton';
import EditButton from '@/app/components/editButton';
import { useRouter } from 'next/navigation';
import './styles.css';

export default function EditApplicationPage({ params }) {
  const { id } = params; // ID заявки из URL
  const [files, setFiles] = useState({
    template: null,
    document1: null,
    document2: null,
    document3: null,
  });
  const [application, setApplication] = useState(null);
  const router = useRouter();

  useEffect(() => {
    const fetchApplication = async () => {
      try {
        const response = await fetch('/api/getApplications');
        if (!response.ok) {
          throw new Error('Ошибка при загрузке заявки');
        }
        const data = await response.json();
        const app = data.find((item) => item.id.toString() === id);
        setApplication(app || null);

        // Заполняем файлы для отображения
        if (app?.files) {
          setFiles({
            template: { name: app.files.template },
            document1: { name: app.files.document1 },
            document2: app.files.document2 ? { name: app.files.document2 } : null,
            document3: app.files.document3 ? { name: app.files.document3 } : null,
          });
        }
      } catch (error) {
        console.error('Ошибка загрузки данных:', error);
      }
    };

    fetchApplication();
  }, [id]);

  const handleFileUpload = (key, file) => {
    setFiles((prev) => ({
      ...prev,
      [key]: file,
    }));
  };

  if (!application) {
    return (
      <div className="container">
        <p>Заявка не найдена.</p>
        <button className="button_back" onClick={() => router.push('/pages/status')}>
          Назад
        </button>
      </div>
    );
  }

  return (
    <div className="container">
      <h1 className="title">Редактирование заявки<br/>№{application.id}</h1>
      <div className="file-upload-section">
        <div className="file-upload-block">
          <p className="file-upload-title">Заполненный шаблон заявления</p>
          <UploadFileButton
            label={files.template ? files.template.name : 'Загрузите файл'}
            onFileUpload={(file) => handleFileUpload('template', file)}
          />
        </div>
        <div className="file-upload-block">
          <p className="file-upload-title">Документ 1</p>
          <UploadFileButton
            label={files.document1 ? files.document1.name : 'Загрузите файл'}
            onFileUpload={(file) => handleFileUpload('document1', file)}
          />
        </div>
        <div className="file-upload-block">
          <p className="file-upload-title">Документ 2</p>
          <UploadFileButton
            label={files.document2 ? files.document2.name : 'Загрузите файл'}
            onFileUpload={(file) => handleFileUpload('document2', file)}
          />
        </div>
        <div className="file-upload-block">
          <p className="file-upload-title">Документ 3</p>
          <UploadFileButton
            label={files.document3 ? files.document3.name : 'Загрузите файл'}
            onFileUpload={(file) => handleFileUpload('document3', file)}
          />
        </div>
      </div>
      <div className="button-container">
        <EditButton id={application.id} files={files} />
        <button
          className="button_back"
          onClick={() => router.push('/pages/status')}
        >
          Назад
        </button>
      </div>
    </div>
  );
}
