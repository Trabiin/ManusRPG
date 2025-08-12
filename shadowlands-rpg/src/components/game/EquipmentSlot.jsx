import React from 'react';

const EquipmentSlot = ({ 
  slotType = 'empty',
  item = null,
  onClick = () => {},
  className = '',
  size = 'default',
  ...props 
}) => {
  const sizeClasses = {
    small: 'w-12 h-12',
    default: 'w-16 h-16',
    large: 'w-20 h-20'
  };
  
  const slotTypeClasses = {
    helmet: 'border-blue-500/50',
    armor: 'border-green-500/50',
    weapon: 'border-red-500/50',
    shield: 'border-yellow-500/50',
    accessory: 'border-purple-500/50',
    empty: 'border-gray-500/50'
  };
  
  const baseClasses = 'inventory-slot relative flex items-center justify-center cursor-pointer transition-all duration-200 rounded-md border-2 bg-gray-800/50 hover:bg-gray-700/50';
  const sizeClass = sizeClasses[size] || sizeClasses.default;
  const slotClass = slotTypeClasses[slotType] || slotTypeClasses.empty;
  const combinedClasses = `${baseClasses} ${sizeClass} ${slotClass} ${className}`.trim();
  
  const handleClick = () => {
    onClick(slotType, item);
  };
  
  return (
    <div
      className={combinedClasses}
      onClick={handleClick}
      title={item ? item.name : `${slotType} slot`}
      {...props}
    >
      {item ? (
        <div className="w-full h-full flex items-center justify-center">
          {item.icon ? (
            <img 
              src={item.icon} 
              alt={item.name}
              className="w-full h-full object-cover rounded-sm"
            />
          ) : (
            <div className="w-8 h-8 bg-gray-600 rounded-sm flex items-center justify-center">
              <span className="text-xs text-gray-300">
                {item.name?.charAt(0) || '?'}
              </span>
            </div>
          )}
          
          {/* Item quality indicator */}
          {item.quality && (
            <div className={`absolute top-0 right-0 w-2 h-2 rounded-full ${
              item.quality === 'legendary' ? 'bg-orange-500' :
              item.quality === 'epic' ? 'bg-purple-500' :
              item.quality === 'rare' ? 'bg-blue-500' :
              item.quality === 'uncommon' ? 'bg-green-500' :
              'bg-gray-500'
            }`} />
          )}
          
          {/* Item level/count indicator */}
          {(item.level || item.count) && (
            <div className="absolute bottom-0 right-0 bg-black/70 text-white text-xs px-1 rounded-tl">
              {item.level || item.count}
            </div>
          )}
        </div>
      ) : (
        <div className="w-8 h-8 flex items-center justify-center text-gray-500">
          {/* Empty slot icon based on type */}
          {slotType === 'helmet' && (
            <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 24 24">
              <path d="M12 2C8.5 2 6 4.5 6 8v4c0 1.1.9 2 2 2h8c1.1 0 2-.9 2-2V8c0-3.5-2.5-6-6-6z"/>
            </svg>
          )}
          {slotType === 'armor' && (
            <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 24 24">
              <path d="M12 1L3 5v6c0 5.55 3.84 10.74 9 12 5.16-1.26 9-6.45 9-12V5l-9-4z"/>
            </svg>
          )}
          {slotType === 'weapon' && (
            <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 24 24">
              <path d="M6.92 5L5 6.92l6.36 6.36-1.42 1.42L3.58 8.34 2.16 9.76l6.36 6.36L7.1 17.54l-1.42-1.42L4.26 17.54 5.68 19l1.42-1.42 1.42 1.42L10.94 17.54l6.36-6.36L19.74 12.6l-1.42-1.42-6.36-6.36L10.54 6.24 6.92 5z"/>
            </svg>
          )}
          {slotType === 'shield' && (
            <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 24 24">
              <path d="M12.5 1.5L5.5 4v5.5c0 4.19 2.89 8.11 6.5 9 3.61-.89 6.5-4.81 6.5-9V4l-6-2.5z"/>
            </svg>
          )}
          {(slotType === 'accessory' || slotType === 'empty') && (
            <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 24 24">
              <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8z"/>
            </svg>
          )}
        </div>
      )}
    </div>
  );
};

export default EquipmentSlot;

