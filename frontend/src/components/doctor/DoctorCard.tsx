import { Link } from 'react-router-dom';
import type { Doctor } from '../../types';
import StarRating from '../ui/StarRating';

interface Props {
  doctor: Doctor;
}

export default function DoctorCard({ doctor }: Props) {
  return (
    <div className="bg-white rounded-xl border border-gray-200 p-5 hover:shadow-md transition-shadow flex gap-4">
      <div className="w-16 h-16 rounded-full bg-gray-100 flex-shrink-0 overflow-hidden">
        {doctor.photo_url ? (
          <img src={doctor.photo_url} alt={`${doctor.first_name} ${doctor.last_name}`} className="w-full h-full object-cover" />
        ) : (
          <div className="w-full h-full flex items-center justify-center text-gray-400 text-2xl">👤</div>
        )}
      </div>

      <div className="flex-1 min-w-0">
        <h3 className="font-semibold text-gray-900">
          {doctor.last_name} {doctor.first_name} {doctor.patronymic}
        </h3>
        <p className="text-sm text-blue-600">{doctor.specialty}</p>
        <p className="text-sm text-gray-500 mt-0.5">Стаж: {doctor.experience_years} лет</p>

        <div className="mt-2">
          <StarRating rating={doctor.rating} count={doctor.reviews_count} size="sm" />
        </div>

        <div className="flex items-center justify-between mt-3">
          <span className="text-sm font-medium text-gray-900">
            от {doctor.consultation_price.toLocaleString()} ₸
          </span>
          <div className="flex gap-2">
            <Link
              to={`/doctors/${doctor.id}`}
              className="text-sm border border-blue-600 text-blue-600 px-3 py-1.5 rounded-lg hover:bg-blue-50 transition-colors"
            >
              Профиль
            </Link>
            <Link
              to={`/doctors/${doctor.id}#appointment`}
              data-testid="doctor-option"
              className="text-sm bg-blue-600 text-white px-3 py-1.5 rounded-lg hover:bg-blue-700 transition-colors"
            >
              Записаться
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}
