import React, { useState } from 'react';
import { Card } from '../ui/card';
import { Badge } from '../ui/badge';
import EquipmentTooltip from './EquipmentTooltip';

const EquipmentSlot = ({ 
  slotName, 
  equipment, 
  character, 
  onEquip, 
  onUnequip, 
  className = "",
  size = "md" 
}) => {
  const [showTooltip, setShowTooltip] = useState(false);
  const [tooltipPosition, setTooltipPosition] = useState({ x: 0, y: 0 });

  const getSlotIcon = (slotName) => {
    const icons = {
      'weapon_main': '⚔️',
      'weapon_off': '🛡️',
      'armor_head': '🪖',
      'armor_chest': '🦺',
      'armor_legs': '👖',
      'armor_feet': '🥾',
      'armor_hands': '🧤',
      'accessory_ring1': '💍',
      'accessory_ring2': '💍',
      'accessory_amulet': '📿'
    };
    return icons[slotName] || '📦';
  };

  const getSlotLabel = (slotName) => {
    const labels = {
      'weapon_main': 'Main Hand',
      'weapon_off': 'Off Hand',
      'armor_head': 'Head',
      'armor_chest': 'Chest',
      'armor_legs': 'Legs',
      'armor_feet': 'Feet',
      'armor_hands': 'Hands',
      'accessory_ring1': 'Ring 1',
      'accessory_ring2': 'Ring 2',
      'accessory_amulet': 'Amulet'
    };
    return labels[slotName] || slotName;
  };

  const getRarityColor = (rarity) => {
    const colors = {
      'Common': 'border-gray-500',
      'Uncommon': 'border-green-500',
      'Rare': 'border-blue-500',
      'Epic': 'border-purple-500',
      'Legendary': 'border-orange-500'
    };
    return colors[rarity] || 'border-gray-500';
  };

  const getCorruptionGlow = (variant) => {
    const glows = {
      'Pure': 'shadow-blue-500/20',
      'Neutral': '',
      'Corrupted': 'shadow-red-500/20'
    };
    return glows[variant] || '';
  };

  const sizeClasses = {
    sm: 'w-12 h-12',
    md: 'w-16 h-16',
    lg: 'w-20 h-20'
  };

  const handleMouseEnter = (e) => {
    if (equipment) {
      setTooltipPosition({ x: e.clientX, y: e.clientY });
      setShowTooltip(true);
    }
  };

  const handleMouseLeave = () => {
    setShowTooltip(false);
  };

  const handleMouseMove = (e) => {
    if (showTooltip) {
      setTooltipPosition({ x: e.clientX, y: e.clientY });
    }
  };

  const handleClick = () => {
    if (equipment && onUnequip) {
      onUnequip(slotName);
    }
  };

  return (
    <>
      <div className={`relative ${className}`}>
        <Card 
          className={`
            ${sizeClasses[size]} 
            flex flex-col items-center justify-center 
            bg-gray-800 border-2 border-gray-600 
            hover:border-gray-500 transition-all duration-200 cursor-pointer
            ${equipment ? getRarityColor(equipment.rarity?.name) : ''}
            ${equipment ? getCorruptionGlow(equipment.corruption_variant?.name) : ''}
            ${equipment ? 'hover:shadow-lg' : ''}
          `}
          onMouseEnter={handleMouseEnter}
          onMouseLeave={handleMouseLeave}
          onMouseMove={handleMouseMove}
          onClick={handleClick}
        >
          {equipment ? (
            <div className="flex flex-col items-center justify-center h-full w-full p-1">
              <div className="text-lg mb-1">{getSlotIcon(slotName)}</div>
              <div className="text-xs text-center text-gray-300 leading-tight">
                {equipment.name.length > 12 
                  ? equipment.name.substring(0, 10) + '...' 
                  : equipment.name
                }
              </div>
              {equipment.rarity && (
                <Badge 
                  className={`
                    text-xs px-1 py-0 mt-1 
                    ${getRarityColor(equipment.rarity.name).replace('border-', 'bg-')} 
                    text-white
                  `}
                >
                  {equipment.rarity.name.charAt(0)}
                </Badge>
              )}
            </div>
          ) : (
            <div className="flex flex-col items-center justify-center h-full w-full text-gray-500">
              <div className="text-lg mb-1">{getSlotIcon(slotName)}</div>
              <div className="text-xs text-center leading-tight">
                {getSlotLabel(slotName)}
              </div>
            </div>
          )}
        </Card>

        {/* Durability indicator */}
        {equipment && equipment.durability < equipment.max_durability && (
          <div className="absolute -bottom-1 left-0 right-0 h-1 bg-gray-700 rounded-full overflow-hidden">
            <div 
              className={`h-full transition-all duration-300 ${
                equipment.durability / equipment.max_durability > 0.5 
                  ? 'bg-green-500' 
                  : equipment.durability / equipment.max_durability > 0.25 
                    ? 'bg-yellow-500' 
                    : 'bg-red-500'
              }`}
              style={{ 
                width: `${(equipment.durability / equipment.max_durability) * 100}%` 
              }}
            />
          </div>
        )}

        {/* Corruption indicator */}
        {equipment && equipment.corruption_effect !== 0 && (
          <div className="absolute -top-1 -right-1 w-3 h-3 rounded-full border border-gray-600">
            <div 
              className={`w-full h-full rounded-full ${
                equipment.corruption_effect > 0 ? 'bg-red-500' : 'bg-blue-500'
              }`}
            />
          </div>
        )}
      </div>

      <EquipmentTooltip
        equipment={equipment}
        character={character}
        position={tooltipPosition}
        visible={showTooltip}
      />
    </>
  );
};

export default EquipmentSlot;

