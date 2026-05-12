import { useState } from 'react';
import { useSearchParams } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import { getDoctors, getSpecialties } from '../api/doctors';
import DoctorCard from '../components/doctor/DoctorCard';

export default function DoctorsPage() {
  const [searchParams] = useSearchParams();
  const [specialty, setSpecialty] = useState(searchParams.get('specialty') || '');
  const [priceMax, setPriceMax] = useState(30000);
  const [page, setPage] = useState(1);

  const { data, isLoading } = useQuery({
    queryKey: ['doctors', { specialty, priceMax, page }],
    queryFn: () => getDoctors({ specialty: specialty || undefined, price_max: priceMax, page, limit: 12 }),
  });

  const { data: specialties } = useQuery({
    queryKey: ['specialties'],
    queryFn: getSpecialties,
  });

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <h1 className="text-2xl font-bold text-gray-900 mb-6">Врачи Алматы</h1>

      <div className="flex flex-col lg:flex-row gap-6">
        <aside className="w-full lg:w-64 flex-shrink-0">
          <div className="bg-white rounded-xl border border-gray-200 p-5 space-y-5">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Специализация</label>
              <select
                value={specialty}
                onChange={(e) => { setSpecialty(e.target.value); setPage(1); }}
                className="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-blue-400"
              >
                <option value="">Все специализации</option>
                {specialties?.map((s) => <option key={s} value={s}>{s}</option>)}
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Цена до: {priceMax.toLocaleString()} ₸
              </label>
              <input
                type="range"
                min={1000}
                max={30000}
                step={1000}
                value={priceMax}
                onChange={(e) => setPriceMax(Number(e.target.value))}
                className="w-full accent-blue-600"
              />
              <div className="flex justify-between text-xs text-gray-400 mt-1">
                <span>1 000 ₸</span>
                <span>30 000 ₸</span>
              </div>
            </div>

            <button
              onClick={() => { setSpecialty(''); setPriceMax(30000); setPage(1); }}
              className="w-full text-sm text-gray-500 border border-gray-200 py-2 rounded-lg hover:bg-gray-50"
            >
              Сбросить
            </button>
          </div>
        </aside>

        <div className="flex-1">
          {isLoading ? (
            <div className="space-y-4">
              {Array.from({ length: 5 }).map((_, i) => (
                <div key={i} className="bg-white rounded-xl border border-gray-200 p-5 animate-pulse h-32" />
              ))}
            </div>
          ) : data?.items.length === 0 ? (
            <div className="text-center py-16 text-gray-400">
              <p className="text-4xl mb-3">👨‍⚕️</p>
              <p>Врачи не найдены. Попробуйте изменить фильтры.</p>
            </div>
          ) : (
            <>
              <p className="text-sm text-gray-500 mb-4">Найдено: {data?.total} врачей</p>
              <div className="space-y-4">
                {data?.items.map((doctor) => (
                  <DoctorCard key={doctor.id} doctor={doctor} />
                ))}
              </div>
              {data && data.pages > 1 && (
                <div className="flex justify-center gap-2 mt-8">
                  <button
                    onClick={() => setPage((p) => Math.max(1, p - 1))}
                    disabled={page === 1}
                    className="px-4 py-2 text-sm border border-gray-200 rounded-lg disabled:opacity-50"
                  >
                    ← Назад
                  </button>
                  <span className="px-4 py-2 text-sm text-gray-500">{page} / {data.pages}</span>
                  <button
                    onClick={() => setPage((p) => p + 1)}
                    disabled={page >= data.pages}
                    className="px-4 py-2 text-sm border border-gray-200 rounded-lg disabled:opacity-50"
                  >
                    Далее →
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
