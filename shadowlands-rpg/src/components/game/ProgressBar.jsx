import React from 'react';

const ProgressBar = ({
  value = 0,
  max = 100,
  type = 'health',
  size = 'md',
  showText = true,
  corruption = 0,
  label = ''
}) => {
  const percentage = Math.min((value / max) * 100, 100);
  const corruptionClass = `corruption-level-${Math.floor(corruption / 25)}`;
  
  const sizeClasses = {
    sm: 'h-4',
    md: 'h-6',
    lg: 'h-8'
  };

  const typeColors = {
    health: 'bg-gradient-to-r from-red-800 to-red-600',
    mana: 'bg-gradient-to-r from-purple-800 to-purple-600',
    corruption: 'bg-gradient-to-r from-gray-800 to-red-800',
    experience: 'bg-gradient-to-r from-yellow-600 to-yellow-400'
  };

  return (
    <div className={`progress-bar w-full ${corruptionClass}`}>
      {label && (
        <div className="text-sm font-medium text-gray-200 mb-1 font-secondary">
          {label}
        </div>
      )}
      <div className={`relative ${sizeClasses[size]} bg-gray-800 border border-gray-600 rounded-full overflow-hidden`}>
        <div 
          className={`h-full transition-all duration-300 ease-out rounded-full ${typeColors[type]}`}
          style={{ width: `${percentage}%` }}
        />
        {showText && (
          <div className="absolute inset-0 flex items-center justify-center">
            <span className="text-xs font-semibold text-white drop-shadow-lg font-secondary">
              {value} / {max}
            </span>
          </div>
        )}
      </div>
    </div>
  );
};

export default ProgressBar;

