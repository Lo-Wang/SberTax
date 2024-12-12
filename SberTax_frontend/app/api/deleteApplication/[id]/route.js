import fs from "fs";
import path from "path";

export async function DELETE(req, { params }) {
  const { id } = params; // Получаем ID из URL
  const filePath = path.join(process.cwd(), "data", "applications.json");

  try {
    // Читаем существующие данные
    const fileData = fs.readFileSync(filePath, "utf8");
    const applications = JSON.parse(fileData);

    // Фильтруем данные, исключая заявку с указанным ID
    const updatedApplications = applications.filter(
      (app) => app.id.toString() !== id
    );

    // Сохраняем обновленные данные
    fs.writeFileSync(filePath, JSON.stringify(updatedApplications, null, 2));

    return new Response(JSON.stringify({ message: "Заявка успешно удалена" }), {
      status: 200,
    });
  } catch (error) {
    console.error("Ошибка при удалении заявки:", error);
    return new Response(
      JSON.stringify({ message: "Ошибка при удалении заявки" }),
      { status: 500 }
    );
  }
}
