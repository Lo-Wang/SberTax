export default function DownloadTemplateButton() {
  const handleDownload = () => {
    // Логика для скачивания файла
    const link = document.createElement('a');
    link.href = '/template/template.docx'; // Путь к файлу
    link.download = 'template.docx';
    link.click();
  };

  return (
    <button className="button" onClick={handleDownload}>
      Шаблон заявления
    </button>
  );
}
