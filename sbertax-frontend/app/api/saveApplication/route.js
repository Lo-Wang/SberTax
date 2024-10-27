import fs from 'fs';
import path from 'path';

export async function POST(req) {
  const newApplication = await req.json();
  newApplication.date = new Date().toISOString(); // Добавляем дату

  const filePath = path.join(process.cwd(), 'data', 'applications.json');

  try {
    // Если файл не существует, создаем пустой массив
    const fileData = fs.existsSync(filePath) ? fs.readFileSync(filePath, 'utf8') : '[]';
    const applications = JSON.parse(fileData);

    // Добавляем новую заявку
    applications.push(newApplication);

    // Сохраняем в файл
    fs.writeFileSync(filePath, JSON.stringify(applications, null, 2));
    return new Response(JSON.stringify({ message: 'Заявка успешно сохранена' }), { status: 200 });
  } catch (error) {
    console.error("Ошибка при сохранении заявки:", error);
    return new Response(JSON.stringify({ message: 'Ошибка при сохранении заявки' }), { status: 500 });
  }
}
