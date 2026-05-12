interface Props {
  rating: number;
  count?: number;
  size?: 'sm' | 'md';
}

export default function StarRating({ rating, count, size = 'md' }: Props) {
  const starSize = size === 'sm' ? 'text-sm' : 'text-base';

  return (
    <div className="flex items-center gap-1">
      <div className={`flex ${starSize}`}>
        {[1, 2, 3, 4, 5].map((star) => (
          <span key={star} className={star <= Math.round(rating) ? 'text-yellow-400' : 'text-gray-300'}>
            ★
          </span>
        ))}
      </div>
      <span className={`${starSize} text-gray-500`}>
        {rating.toFixed(1)}{count !== undefined && ` (${count})`}
      </span>
    </div>
  );
}
