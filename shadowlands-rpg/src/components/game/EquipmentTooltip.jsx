import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '../ui/card';
import { Badge } from '../ui/badge';
import { Separator } from '../ui/separator';

const EquipmentTooltip = ({ equipment, character, position, visible }) => {
  if (!visible || !equipment) return null;

  const getRarityColor = (rarity) => {
    const colors = {
      'Common': 'bg-gray-500',
      'Uncommon': 'bg-green-500',
      'Rare': 'bg-blue-500',
      'Epic': 'bg-purple-500',
      'Legendary': 'bg-orange-500'
    };
    return colors[rarity] || 'bg-gray-500';
  };

  const getCorruptionColor = (variant) => {
    const colors = {
      'Pure': 'text-blue-300',
      'Neutral': 'text-gray-300',
      'Corrupted': 'text-red-300'
    };
    return colors[variant] || 'text-gray-300';
  };

  const canEquip = equipment.can_equip;
  const requirements = equipment.requirements;

  return (
    <div
      className="fixed z-50 pointer-events-none"
      style={{
        left: position.x + 10,
        top: position.y - 10,
        maxWidth: '320px'
      }}
    >
      <Card className="bg-gray-900 border-gray-700 text-white shadow-2xl">
        <CardHeader className="pb-2">
          <div className="flex items-center justify-between">
            <CardTitle className={`text-lg ${getCorruptionColor(equipment.corruption_variant?.name)}`}>
              {equipment.name}
            </CardTitle>
            <Badge className={`${getRarityColor(equipment.rarity?.name)} text-white`}>
              {equipment.rarity?.name}
            </Badge>
          </div>
          <div className="text-sm text-gray-400">
            {equipment.type} • Level {equipment.level}
          </div>
        </CardHeader>

        <CardContent className="space-y-3">
          {/* Stats */}
          <div>
            <h4 className="text-sm font-semibold text-gray-300 mb-2">Stats</h4>
            <div className="grid grid-cols-2 gap-1 text-sm">
              {Object.entries(equipment.stats || {}).map(([stat, value]) => {
                if (value === 0) return null;
                return (
                  <div key={stat} className="flex justify-between">
                    <span className="text-gray-400 capitalize">
                      {stat.replace('_', ' ')}:
                    </span>
                    <span className="text-green-400">+{value}</span>
                  </div>
                );
              })}
            </div>
          </div>

          {/* Requirements */}
          <div>
            <h4 className="text-sm font-semibold text-gray-300 mb-2">Requirements</h4>
            <div className="space-y-1 text-sm">
              <div className="flex justify-between">
                <span className="text-gray-400">Level:</span>
                <span className={character?.level >= requirements?.level ? 'text-green-400' : 'text-red-400'}>
                  {requirements?.level}
                </span>
              </div>
              {requirements?.might > 0 && (
                <div className="flex justify-between">
                  <span className="text-gray-400">Might:</span>
                  <span className={character?.might >= requirements?.might ? 'text-green-400' : 'text-red-400'}>
                    {requirements?.might}
                  </span>
                </div>
              )}
              {requirements?.intellect > 0 && (
                <div className="flex justify-between">
                  <span className="text-gray-400">Intellect:</span>
                  <span className={character?.intellect >= requirements?.intellect ? 'text-green-400' : 'text-red-400'}>
                    {requirements?.intellect}
                  </span>
                </div>
              )}
              {requirements?.will > 0 && (
                <div className="flex justify-between">
                  <span className="text-gray-400">Will:</span>
                  <span className={character?.will >= requirements?.will ? 'text-green-400' : 'text-red-400'}>
                    {requirements?.will}
                  </span>
                </div>
              )}
              {requirements?.shadow > 0 && (
                <div className="flex justify-between">
                  <span className="text-gray-400">Shadow:</span>
                  <span className={character?.shadow >= requirements?.shadow ? 'text-green-400' : 'text-red-400'}>
                    {requirements?.shadow}
                  </span>
                </div>
              )}
              {requirements?.corruption_min > 0 && (
                <div className="flex justify-between">
                  <span className="text-gray-400">Min Corruption:</span>
                  <span className={character?.corruption >= requirements?.corruption_min ? 'text-green-400' : 'text-red-400'}>
                    {requirements?.corruption_min}
                  </span>
                </div>
              )}
              {requirements?.corruption_max < 100 && (
                <div className="flex justify-between">
                  <span className="text-gray-400">Max Corruption:</span>
                  <span className={character?.corruption <= requirements?.corruption_max ? 'text-green-400' : 'text-red-400'}>
                    {requirements?.corruption_max}
                  </span>
                </div>
              )}
            </div>
          </div>

          {/* Special Properties */}
          {equipment.special_properties && equipment.special_properties.length > 0 && (
            <div>
              <h4 className="text-sm font-semibold text-gray-300 mb-2">Special Properties</h4>
              <div className="space-y-1">
                {equipment.special_properties.map((property, index) => (
                  <div key={index} className="text-sm text-yellow-400">
                    • {property}
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Enchantments */}
          {equipment.enchantments && equipment.enchantments.length > 0 && (
            <div>
              <h4 className="text-sm font-semibold text-gray-300 mb-2">Enchantments</h4>
              <div className="space-y-1">
                {equipment.enchantments.map((enchantment, index) => (
                  <div key={index} className="text-sm text-purple-400">
                    • {enchantment.name}
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Corruption Effect */}
          {equipment.corruption_effect !== 0 && (
            <div>
              <Separator className="bg-gray-700" />
              <div className="flex justify-between text-sm">
                <span className="text-gray-400">Corruption Effect:</span>
                <span className={equipment.corruption_effect > 0 ? 'text-red-400' : 'text-blue-400'}>
                  {equipment.corruption_effect > 0 ? '+' : ''}{(equipment.corruption_effect * 100).toFixed(1)}%
                </span>
              </div>
            </div>
          )}

          {/* Durability */}
          <div>
            <Separator className="bg-gray-700" />
            <div className="flex justify-between text-sm">
              <span className="text-gray-400">Durability:</span>
              <span className="text-gray-300">
                {equipment.durability}/{equipment.max_durability}
              </span>
            </div>
          </div>

          {/* Equip Status */}
          <div>
            <Separator className="bg-gray-700" />
            <div className={`text-sm text-center ${canEquip ? 'text-green-400' : 'text-red-400'}`}>
              {canEquip ? '✓ Can Equip' : `✗ ${equipment.equip_reason || 'Cannot Equip'}`}
            </div>
          </div>

          {/* Description */}
          {equipment.description && (
            <div>
              <Separator className="bg-gray-700" />
              <p className="text-sm text-gray-300 italic">
                {equipment.description}
              </p>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
};

export default EquipmentTooltip;

