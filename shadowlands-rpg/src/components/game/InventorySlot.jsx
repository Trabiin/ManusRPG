import React from 'react';

const InventorySlot = ({
  item = null,
  size = 'md',
  onClick = () => {},
  onRightClick = () => {}
}) => {
  const sizeClasses = {
    sm: 'w-10 h-10',
    md: 'w-14 h-14',
    lg: 'w-18 h-18'
  };

  const rarityColors = {
    poor: 'border-gray-500 hover:shadow-gray-500/50',
    common: 'border-white hover:shadow-white/50',
    uncommon: 'border-green-500 hover:shadow-green-500/50',
    rare: 'border-blue-500 hover:shadow-blue-500/50',
    epic: 'border-purple-500 hover:shadow-purple-500/50',
    legendary: 'border-orange-500 hover:shadow-orange-500/50'
  };

  const handleClick = () => {
    if (item && onClick) onClick(item);
  };
  
  const handleRightClick = (e) => {
    e.preventDefault();
    if (item && onRightClick) onRightClick(item);
  };

  return (
    <div 
      className={`
        inventory-slot ${sizeClasses[size]} 
        bg-gray-800 border-2 border-gray-600 rounded-md 
        cursor-pointer transition-all duration-200 
        flex items-center justify-center relative
        hover:border-yellow-500 hover:shadow-lg hover:shadow-yellow-500/30
        ${item ? rarityColors[item.rarity] || 'border-gray-600' : ''}
      `}
      onClick={handleClick}
      onContextMenu={handleRightClick}
    >
      {item && (
        <>
          <img 
            src={item.icon || '/api/placeholder/40/40'} 
            alt={item.name}
            className="w-4/5 h-4/5 object-contain"
            onError={(e) => {
              e.target.src = 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDAiIGhlaWdodD0iNDAiIHZpZXdCb3g9IjAgMCA0MCA0MCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHJlY3Qgd2lkdGg9IjQwIiBoZWlnaHQ9IjQwIiBmaWxsPSIjNEE0QTRBIi8+CjxyZWN0IHg9IjEwIiB5PSIxMCIgd2lkdGg9IjIwIiBoZWlnaHQ9IjIwIiBmaWxsPSIjNkI3Mjc5Ii8+Cjwvc3ZnPg==';
            }}
          />
          {item.quantity && item.quantity > 1 && (
            <div className="absolute bottom-0.5 right-0.5 bg-black/80 text-white text-xs font-bold px-1 rounded min-w-4 text-center">
              {item.quantity}
            </div>
          )}
          {item.corruption && item.corruption > 0 && (
            <div className="absolute top-0.5 left-0.5 w-2 h-2 bg-red-600 rounded-full shadow-lg shadow-red-600/50" />
          )}
        </>
      )}
    </div>
  );
};

export default InventorySlot;

