import { Link } from 'react-router-dom';
import type { Clinic } from '../../types';
import StarRating from '../ui/StarRating';

interface Props {
  clinic: Clinic;
}

export default function ClinicCard({ clinic }: Props) {
  return (
    <div
      data-testid="clinic-card"
      className="bg-white rounded-xl border border-gray-200 p-5 hover:shadow-md transition-shadow flex flex-col gap-3"
    >
      <div className="flex items-start gap-4">
        <div className="w-14 h-14 rounded-lg bg-blue-50 flex items-center justify-center flex-shrink-0 overflow-hidden">
          {clinic.logo_url ? (
            <img src={clinic.logo_url} alt={clinic.name} className="w-full h-full object-cover" />
          ) : (
            <span className="text-blue-600 text-xl font-bold">{clinic.name[0]}</span>
          )}
        </div>
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2">
            <h3 className="font-semibold text-gray-900 truncate">{clinic.name}</h3>
            {clinic.is_verified && (
              <span className="text-blue-600 text-xs bg-blue-50 px-2 py-0.5 rounded-full flex-shrink-0">✓ Верифицировано</span>
            )}
          </div>
          <p className="text-sm text-gray-500 mt-0.5">{clinic.address}</p>
          <p className="text-xs text-gray-400">{clinic.district}</p>
        </div>
      </div>

      <StarRating rating={clinic.rating} count={clinic.reviews_count} size="sm" />

      {clinic.phone && (
        <a href={`tel:${clinic.phone}`} className="text-sm text-blue-600 hover:underline">
          {clinic.phone}
        </a>
      )}

      <div className="flex gap-2 mt-1">
        <Link
          to={`/clinics/${clinic.id}`}
          className="flex-1 text-center text-sm border border-blue-600 text-blue-600 py-2 rounded-lg hover:bg-blue-50 transition-colors"
        >
          Подробнее
        </Link>
        <Link
          to={`/clinics/${clinic.id}#appointment`}
          data-testid="btn-book"
          className="flex-1 text-center text-sm bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700 transition-colors"
        >
          Записаться
        </Link>
      </div>
    </div>
  );
}
