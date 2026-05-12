import { useState } from 'react';
import { useSearchParams } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import { getClinics } from '../api/clinics';
import ClinicCard from '../components/clinic/ClinicCard';

const DISTRICTS = ['Алмалинский', 'Бостандыкский', 'Медеуский', 'Ауэзовский', 'Жетысуский', 'Турксибский'];

export default function ClinicsPage() {
  const [searchParams, setSearchParams] = useSearchParams();
  const [search, setSearch] = useState(searchParams.get('search') || '');
  const [district, setDistrict] = useState('');
  const [rating, setRating] = useState(0);
  const page = Number(searchParams.get('page') || 1);

  const { data, isLoading } = useQuery({
    queryKey: ['clinics', { search, district, rating, page }],
    queryFn: () => getClinics({ search, district: district || undefined, rating: rating || undefined, page, limit: 12 }),
  });

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    setSearchParams({ search, page: '1' });
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <h1 className="text-2xl font-bold text-gray-900 mb-6">Клиники Алматы</h1>

      <div className="flex flex-col lg:flex-row gap-6">
        <aside className="w-full lg:w-64 flex-shrink-0">
          <div className="bg-white rounded-xl border border-gray-200 p-5 space-y-5">
            <form onSubmit={handleSearch}>
              <label className="block text-sm font-medium text-gray-700 mb-1">Поиск</label>
              <input
                data-testid="search-input"
                type="text"
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                placeholder="Название клиники..."
                className="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-blue-400"
              />
            </form>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Район</label>
              <div className="space-y-1">
                {DISTRICTS.map((d) => (
                  <label key={d} className="flex items-center gap-2 text-sm text-gray-600 cursor-pointer">
                    <input
                      type="radio"
                      name="district"
                      checked={district === d}
                      onChange={() => setDistrict(d)}
                      data-testid={`filter-district-${d}`}
                      className="text-blue-600"
                    />
                    {d}
                  </label>
                ))}
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Рейтинг от</label>
              <div className="flex gap-1">
                {[1, 2, 3, 4, 5].map((r) => (
                  <button
                    key={r}
                    onClick={() => setRating(rating === r ? 0 : r)}
                    className={`text-lg ${r <= rating ? 'text-yellow-400' : 'text-gray-300'}`}
                  >
                    ★
                  </button>
                ))}
              </div>
            </div>

            <button
              onClick={() => { setDistrict(''); setRating(0); setSearch(''); }}
              className="w-full text-sm text-gray-500 border border-gray-200 py-2 rounded-lg hover:bg-gray-50"
            >
              Сбросить фильтры
            </button>
          </div>
        </aside>

        <div className="flex-1">
          {isLoading ? (
            <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-3 gap-4">
              {Array.from({ length: 6 }).map((_, i) => (
                <div key={i} className="bg-white rounded-xl border border-gray-200 p-5 animate-pulse h-48" />
              ))}
            </div>
          ) : data?.items.length === 0 ? (
            <div className="text-center py-16 text-gray-400">
              <p className="text-4xl mb-3">🏥</p>
              <p>Клиники не найдены. Попробуйте изменить фильтры.</p>
            </div>
          ) : (
            <>
              <p className="text-sm text-gray-500 mb-4">Найдено: {data?.total} клиник</p>
              <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-3 gap-4">
                {data?.items.map((clinic) => (
                  <ClinicCard key={clinic.id} clinic={clinic} />
                ))}
              </div>

              {data && data.pages > 1 && (
                <div className="flex justify-center gap-2 mt-8">
                  <button
                    data-testid="pagination-next"
                    onClick={() => setSearchParams({ page: String(page + 1) })}
                    disabled={page >= data.pages}
                    className="px-4 py-2 text-sm border border-gray-200 rounded-lg hover:bg-gray-50 disabled:opacity-50"
                  >
                    Следующая →
                  </button>
                </div>
              )}
            </>
          )}
        </div>
      </div>
    </div>
  );
}
