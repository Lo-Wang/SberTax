import fs from 'fs';
import path from 'path';

export async function POST(req) {
  const updatedApplication = await req.json();
  const filePath = path.join(process.cwd(), 'data', 'applications.json');

  try {
    const fileData = fs.readFileSync(filePath, 'utf8');
    const applications = JSON.parse(fileData);

    // Обновляем заявку по ID
    const index = applications.findIndex((app) => app.id === updatedApplication.id);
    if (index === -1) {
      return new Response(JSON.stringify({ message: 'Заявка не найдена' }), { status: 404 });
    }

    applications[index] = { ...applications[index], ...updatedApplication, status: 'Отправлено' };

    fs.writeFileSync(filePath, JSON.stringify(applications, null, 2));
    return new Response(JSON.stringify({ message: 'Заявка успешно обновлена' }), { status: 200 });
  } catch (error) {
    console.error("Ошибка при редактировании заявки:", error);
    return new Response(JSON.stringify({ message: 'Ошибка при редактировании заявки' }), { status: 500 });
  }
}
