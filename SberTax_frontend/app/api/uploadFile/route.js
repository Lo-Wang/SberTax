import fs from 'fs';
import path from 'path';

export async function POST(req) {
  try {
    const data = await req.formData(); // Получаем данные формы
    const file = data.get('file');

    if (!file) {
      console.error("Файл не был загружен");
      return new Response(JSON.stringify({ message: 'Файл не был загружен' }), { status: 400 });
    }

    const uploadsDir = path.join(process.cwd(), 'uploads');
    
    // Проверяем, существует ли папка для загрузок, если нет - создаем
    if (!fs.existsSync(uploadsDir)) {
      fs.mkdirSync(uploadsDir);
    }

    const filePath = path.join(uploadsDir, file.name); // Путь к загруженному файлу

    // Используем поток для записи файла
    const fileStream = fs.createWriteStream(filePath);
    const reader = file.stream().getReader();

    const writeFile = async () => {
      const { done, value } = await reader.read();
      if (done) {
        fileStream.end(); // Закрываем поток
        console.log("Файл успешно загружен:", filePath);
        return new Response(JSON.stringify({ message: 'Файл успешно загружен' }), { status: 200 });
      }
      fileStream.write(value); // Записываем данные в файл
      writeFile(); // Продолжаем запись
    };

    writeFile();

  } catch (error) {
    console.error("Ошибка при загрузке файла:", error); // Выводим ошибку в консоль
    return new Response(JSON.stringify({ message: 'Ошибка при загрузке файла: ' + error.message }), { status: 500 });
  }
}
