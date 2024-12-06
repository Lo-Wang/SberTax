import fs from 'fs';
import path from 'path';

export async function POST(req) {
  try {
    const body = await req.json();

    if (!body || typeof body !== 'object') {
      throw new Error('Неверный формат данных');
    }

    // Инициализация объекта
    const newApplication = {
      ...body,
      submissionDate: new Date().toISOString(), // Добавляем дату
    };

    const applicationsFilePath = path.join(process.cwd(), 'data', 'applications.json');
    const uploadsDir = path.join(process.cwd(), 'uploads');

    // Проверяем наличие папки uploads, если нет — создаем
    if (!fs.existsSync(uploadsDir)) {
      fs.mkdirSync(uploadsDir);
    }

    // Путь к папке с ID заявки
    const applicationDir = path.join(uploadsDir, newApplication.id.toString());

    // Создаем папку для заявки, если она еще не существует
    if (!fs.existsSync(applicationDir)) {
      fs.mkdirSync(applicationDir);
    }

    // Сохраняем файлы (если переданы)
    if (newApplication.files) {
      for (const [key, fileName] of Object.entries(newApplication.files)) {
        if (fileName) {
          const filePath = path.join(applicationDir, fileName);
          fs.writeFileSync(filePath, `Содержимое файла ${fileName}`); // Заглушка для содержимого
        }
      }
    }

    // Читаем текущий JSON
    const fileData = fs.existsSync(applicationsFilePath) ? fs.readFileSync(applicationsFilePath, 'utf8') : '[]';
    const applications = JSON.parse(fileData);

    // Добавляем новую заявку
    applications.push(newApplication);

    // Сохраняем JSON
    fs.writeFileSync(applicationsFilePath, JSON.stringify(applications, null, 2));

    return new Response(JSON.stringify({ message: 'Заявка успешно сохранена' }), { status: 200 });
  } catch (error) {
    console.error("Ошибка при сохранении заявки:", error.message);
    return new Response(JSON.stringify({ message: 'Ошибка при сохранении заявки', error: error.message }), { status: 500 });
  }
}
