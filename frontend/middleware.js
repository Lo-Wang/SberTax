import { NextResponse } from 'next/server';

export function middleware(req) {
  const token = req.cookies.get('token'); // Получаем токен из куки

  // Определяем защищенные маршруты
  const protectedPaths = ['/pages/dashboard', '/pages/status', '/pages/transaction', '/pages/submit-application'];

  // Проверяем, если пользователь пытается получить доступ к защищенной странице
  if (protectedPaths.some(path => req.nextUrl.pathname.startsWith(path)) && !token) {
    // Если токена нет, перенаправляем на страницу авторизации
    return NextResponse.redirect(new URL('/pages/authorization', req.url));
  }

  // Если все проверки пройдены, продолжаем
  return NextResponse.next();
}

// Настройка matcher для применения middleware
export const config = {
  matcher: ['/pages/dashboard/:path*', '/pages/status/:path*', '/pages/transaction/:path*', '/pages/submit-application/:path*'],
};