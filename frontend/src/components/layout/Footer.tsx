import { Link } from 'react-router-dom';

export default function Footer() {
  return (
    <footer className="bg-gray-900 text-gray-400 mt-auto">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          <div>
            <span className="text-white text-xl font-bold">MedFind</span>
            <p className="mt-2 text-sm">Найдите лучшего врача в Алматы</p>
          </div>
          <div>
            <h4 className="text-white font-medium mb-3">Сервис</h4>
            <ul className="space-y-2 text-sm">
              <li><Link to="/clinics" className="hover:text-white">Клиники</Link></li>
              <li><Link to="/doctors" className="hover:text-white">Врачи</Link></li>
              <li><Link to="/services" className="hover:text-white">Услуги</Link></li>
            </ul>
          </div>
          <div>
            <h4 className="text-white font-medium mb-3">Пациентам</h4>
            <ul className="space-y-2 text-sm">
              <li><Link to="/register" className="hover:text-white">Регистрация</Link></li>
              <li><Link to="/login" className="hover:text-white">Войти</Link></li>
            </ul>
          </div>
          <div>
            <h4 className="text-white font-medium mb-3">Контакты</h4>
            <p className="text-sm">Алматы, Казахстан</p>
            <p className="text-sm mt-1">info@medfind.kz</p>
          </div>
        </div>
        <div className="border-t border-gray-800 mt-8 pt-8 text-sm text-center">
          © 2026 MedFind. Все права защищены.
        </div>
      </div>
    </footer>
  );
}
