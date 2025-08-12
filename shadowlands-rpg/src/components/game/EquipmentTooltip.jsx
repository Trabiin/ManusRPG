import React from 'react';

const EquipmentTooltip = ({ 
  item,
  visible = false,
  position = { x: 0, y: 0 },
  className = '',
  ...props 
}) => {
  if (!visible || !item) {
    return null;
  }
  
  const rarityColors = {
    poor: 'text-gray-400 border-gray-400',
    common: 'text-white border-white',
    uncommon: 'text-green-400 border-green-400',
    rare: 'text-blue-400 border-blue-400',
    epic: 'text-purple-400 border-purple-400',
    legendary: 'text-orange-400 border-orange-400'
  };
  
  const rarityClass = rarityColors[item.quality] || rarityColors.common;
  
  const tooltipStyle = {
    position: 'fixed',
    left: position.x + 10,
    top: position.y - 10,
    zIndex: 1000,
    pointerEvents: 'none'
  };
  
  return (
    <div
      style={tooltipStyle}
      className={`bg-gray-900 border-2 rounded-lg p-3 shadow-lg max-w-xs ${rarityClass} ${className}`}
      {...props}
    >
      {/* Item name */}
      <div className={`font-bold text-lg mb-2 ${rarityClass.split(' ')[0]}`}>
        {item.name}
      </div>
      
      {/* Item type and level */}
      <div className="text-gray-300 text-sm mb-2">
        {item.type} {item.level && `(Level ${item.level})`}
      </div>
      
      {/* Item stats */}
      {item.stats && (
        <div className="mb-2">
          {Object.entries(item.stats).map(([stat, value]) => (
            <div key={stat} className="text-sm text-gray-200">
              <span className="text-green-400">+{value}</span> {stat}
            </div>
          ))}
        </div>
      )}
      
      {/* Item description */}
      {item.description && (
        <div className="text-gray-300 text-sm italic border-t border-gray-600 pt-2 mt-2">
          {item.description}
        </div>
      )}
      
      {/* Item value */}
      {item.value && (
        <div className="text-yellow-400 text-sm mt-2">
          Value: {item.value} gold
        </div>
      )}
      
      {/* Item requirements */}
      {item.requirements && (
        <div className="text-red-400 text-sm mt-2">
          Requires: {item.requirements}
        </div>
      )}
      
      {/* Item effects */}
      {item.effects && item.effects.length > 0 && (
        <div className="mt-2">
          {item.effects.map((effect, index) => (
            <div key={index} className="text-blue-300 text-sm">
              {effect}
            </div>
          ))}
        </div>
      )}
      
      {/* Item set bonus */}
      {item.setBonus && (
        <div className="text-purple-300 text-sm mt-2 border-t border-gray-600 pt-2">
          Set Bonus: {item.setBonus}
        </div>
      )}
    </div>
  );
};

export default EquipmentTooltip;

