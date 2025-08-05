import React from 'react';

const CharacterPortrait = ({ 
  imageUrl = '/api/placeholder/120/120',
  name = 'Unknown Drifter',
  level = 1,
  corruption = 0,
  size = 'md',
  showCorruptionEffects = true 
}) => {
  const corruptionLevel = Math.floor(corruption / 25);
  
  const sizeClasses = {
    sm: 'w-16 h-16',
    md: 'w-24 h-24',
    lg: 'w-32 h-32'
  };

  return (
    <div className={`character-portrait ${sizeClasses[size]} relative`}>
      <div className="relative w-full h-full rounded-lg overflow-hidden border-2 border-gray-600">
        <img 
          src={imageUrl} 
          alt={name}
          className="w-full h-full object-cover"
          onError={(e) => {
            e.target.src = 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTIwIiBoZWlnaHQ9IjEyMCIgdmlld0JveD0iMCAwIDEyMCAxMjAiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxyZWN0IHdpZHRoPSIxMjAiIGhlaWdodD0iMTIwIiBmaWxsPSIjMkMyQzJDIi8+CjxjaXJjbGUgY3g9IjYwIiBjeT0iNDUiIHI9IjE1IiBmaWxsPSIjNEE0QTRBIi8+CjxwYXRoIGQ9Ik0zMCA5MEM0MCA4MCA4MCA4MCA5MCA5MEw5MCA5MEgzMFoiIGZpbGw9IiM0QTRBNEEiLz4KPC9zdmc+';
          }}
        />
        {showCorruptionEffects && corruptionLevel > 0 && (
          <div className={`absolute inset-0 bg-red-900 opacity-${corruptionLevel * 10} mix-blend-multiply`} />
        )}
      </div>
      <div className="mt-2 text-center">
        <div className="text-sm font-semibold text-gray-200 font-primary">{name}</div>
        <div className="text-xs text-gray-400">Level {level}</div>
      </div>
    </div>
  );
};

export default CharacterPortrait;

