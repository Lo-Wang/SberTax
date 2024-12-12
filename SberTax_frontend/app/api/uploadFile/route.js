import fs from 'fs';
import path from 'path';

export async function POST(req) {
  const formData = await req.formData();
  const file = formData.get('file'); // Получаем файл из формы

  // Проверка типа файла
  const allowedTypes = ['image/jpeg', 'image/png', 'application/pdf'];
  if (!allowedTypes.includes(file.type)) {
    return new Response(JSON.stringify({ message: 'Неподдерживаемый тип файла' }), { status: 400 });
  }

  // Путь для сохранения файла
  const uploadsDir = path.join(process.cwd(), 'uploads');
  const filePath = path.join(uploadsDir, file.name);

  // Убедимся, что директория uploads существует
  if (!fs.existsSync(uploadsDir)) {
    fs.mkdirSync(uploadsDir);
  }

  try {
    // Записываем файл
    const fileBuffer = await file.arrayBuffer();
    fs.writeFileSync(filePath, Buffer.from(fileBuffer));

    return new Response(JSON.stringify({ message: 'Файл успешно загружен' }), { status: 200 });
  } catch (error) {
    console.error('Ошибка при загрузке файла:', error);
    return new Response(JSON.stringify({ message: 'Ошибка при загрузке файла' }), { status: 500 });
  }
}
