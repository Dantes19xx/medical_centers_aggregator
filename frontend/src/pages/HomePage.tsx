import { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const SPECIALTIES = [
  { name: 'Терапевт', icon: '🩺' },
  { name: 'Кардиолог', icon: '❤️' },
  { name: 'Педиатр', icon: '👶' },
  { name: 'Невролог', icon: '🧠' },
  { name: 'Хирург', icon: '🔪' },
  { name: 'Офтальмолог', icon: '👁️' },
  { name: 'Дерматолог', icon: '🧴' },
  { name: 'Гинеколог', icon: '🌸' },
  { name: 'Ортопед', icon: '🦴' },
  { name: 'Стоматолог', icon: '🦷' },
  { name: 'Эндокринолог', icon: '⚗️' },
  { name: 'Уролог', icon: '💊' },
];

export default function HomePage() {
  const [search, setSearch] = useState('');
  const navigate = useNavigate();

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    if (search.trim()) navigate(`/clinics?search=${encodeURIComponent(search)}`);
  };

  return (
    <div>
      <section className="bg-gradient-to-br from-blue-600 to-blue-800 text-white py-20 px-4">
        <div className="max-w-3xl mx-auto text-center">
          <h1 className="text-4xl sm:text-5xl font-bold mb-4">
            Найдите лучшего врача в Алматы
          </h1>
          <p className="text-blue-100 text-lg mb-8">
            Более 100 клиник и 500 врачей — запишитесь онлайн за 2 минуты
          </p>

          <form onSubmit={handleSearch} className="flex gap-2 max-w-xl mx-auto">
            <input
              data-testid="search-input"
              type="text"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              placeholder="Клиника, врач или услуга..."
              className="flex-1 px-4 py-3 rounded-xl text-gray-900 text-sm focus:outline-none focus:ring-2 focus:ring-blue-300"
            />
            <button
              type="submit"
              className="bg-green-500 hover:bg-green-600 text-white font-semibold px-6 py-3 rounded-xl transition-colors"
            >
              Найти
            </button>
          </form>
        </div>
      </section>

      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <h2 className="text-2xl font-bold text-gray-900 mb-8 text-center">Выберите специализацию</h2>
        <div className="grid grid-cols-3 sm:grid-cols-4 md:grid-cols-6 gap-4">
          {SPECIALTIES.map((s) => (
            <button
              key={s.name}
              onClick={() => navigate(`/doctors?specialty=${encodeURIComponent(s.name)}`)}
              className="flex flex-col items-center gap-2 p-4 bg-white rounded-xl border border-gray-200 hover:border-blue-400 hover:shadow-sm transition-all"
            >
              <span className="text-3xl">{s.icon}</span>
              <span className="text-xs text-gray-700 text-center font-medium">{s.name}</span>
            </button>
          ))}
        </div>
      </section>

      <section className="bg-gray-50 py-16 px-4">
        <div className="max-w-4xl mx-auto">
          <h2 className="text-2xl font-bold text-gray-900 mb-12 text-center">Как это работает</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {[
              { step: '1', title: 'Найдите клинику', desc: 'Используйте поиск и фильтры для выбора подходящей клиники', icon: '🔍' },
              { step: '2', title: 'Выберите врача', desc: 'Посмотрите профили врачей, их специализацию и отзывы', icon: '👨‍⚕️' },
              { step: '3', title: 'Запишитесь онлайн', desc: 'Выберите удобное время и заполните форму записи', icon: '📅' },
            ].map((item) => (
              <div key={item.step} className="text-center">
                <div className="w-16 h-16 bg-blue-600 rounded-full flex items-center justify-center text-white text-2xl mx-auto mb-4">
                  {item.icon}
                </div>
                <h3 className="font-semibold text-gray-900 mb-2">{item.title}</h3>
                <p className="text-sm text-gray-500">{item.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>
    </div>
  );
}
