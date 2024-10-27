import fs from 'fs';
import path from 'path';

export async function GET(req) {
    const filePath = path.join(process.cwd(), 'data', 'applications.json');

    try {
        const fileData = fs.readFileSync(filePath, 'utf8');
        const applications = JSON.parse(fileData);

        // Сортируем массив по дате отправки в обратном порядке
        applications.sort((a, b) => new Date(b.date) - new Date(a.date));
        
        return new Response(JSON.stringify(applications), { status: 200 });
    } catch (error) {
        console.error("Ошибка при получении заявок:", error);
        return new Response(JSON.stringify({ message: 'Ошибка при получении заявок' }), { status: 500 });
    }
}
