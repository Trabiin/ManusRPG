import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '../ui/card';
import { Button } from '../ui/button';
import { Badge } from '../ui/badge';
import { Separator } from '../ui/separator';
import EquipmentSlot from './EquipmentSlot';

const CharacterEquipment = ({ 
  character, 
  equippedItems = {}, 
  onUnequipItem, 
  className = "" 
}) => {
  const [totalStats, setTotalStats] = useState({});

  useEffect(() => {
    // Calculate total stats from equipped items
    const stats = {
      might: character?.might || 0,
      intellect: character?.intellect || 0,
      will: character?.will || 0,
      shadow: character?.shadow || 0,
      health: character?.health || 0,
      mana: character?.mana || 0,
      damage: 0,
      defense: 0,
      corruption_resistance: 0
    };

    Object.values(equippedItems).forEach(item => {
      if (item && item.stats) {
        Object.entries(item.stats).forEach(([stat, value]) => {
          if (stats.hasOwnProperty(stat)) {
            stats[stat] += value;
          }
        });
      }
    });

    setTotalStats(stats);
  }, [character, equippedItems]);

  const equipmentSlots = [
    { name: 'weapon_main', label: 'Main Hand', position: 'top-left' },
    { name: 'weapon_off', label: 'Off Hand', position: 'top-right' },
    { name: 'armor_head', label: 'Head', position: 'center-top' },
    { name: 'armor_chest', label: 'Chest', position: 'center' },
    { name: 'armor_legs', label: 'Legs', position: 'center-bottom' },
    { name: 'armor_feet', label: 'Feet', position: 'bottom' },
    { name: 'armor_hands', label: 'Hands', position: 'sides' },
    { name: 'accessory_ring1', label: 'Ring 1', position: 'bottom-left' },
    { name: 'accessory_ring2', label: 'Ring 2', position: 'bottom-right' },
    { name: 'accessory_amulet', label: 'Amulet', position: 'top-center' }
  ];

  const getStatColor = (baseStat, totalStat) => {
    if (totalStat > baseStat) return 'text-green-400';
    if (totalStat < baseStat) return 'text-red-400';
    return 'text-gray-300';
  };

  const getStatBonus = (baseStat, totalStat) => {
    const bonus = totalStat - baseStat;
    if (bonus === 0) return '';
    return bonus > 0 ? ` (+${bonus})` : ` (${bonus})`;
  };

  return (
    <Card className={`bg-gray-900 border-gray-700 ${className}`}>
      <CardHeader>
        <CardTitle className="text-white flex items-center justify-between">
          <span>Equipment</span>
          <Badge variant="outline" className="text-gray-300">
            {character?.name || 'Character'} - Level {character?.level || 1}
          </Badge>
        </CardTitle>
      </CardHeader>

      <CardContent className="space-y-6">
        {/* Equipment Layout */}
        <div className="relative">
          {/* Character Silhouette Layout */}
          <div className="grid grid-cols-5 gap-2 max-w-md mx-auto">
            {/* Row 1: Amulet */}
            <div className="col-start-3">
              <EquipmentSlot
                slotName="accessory_amulet"
                equipment={equippedItems.accessory_amulet}
                character={character}
                onUnequip={onUnequipItem}
                size="sm"
              />
            </div>

            {/* Row 2: Main Hand, Head, Off Hand */}
            <div className="col-start-1">
              <EquipmentSlot
                slotName="weapon_main"
                equipment={equippedItems.weapon_main}
                character={character}
                onUnequip={onUnequipItem}
              />
            </div>
            <div className="col-start-3">
              <EquipmentSlot
                slotName="armor_head"
                equipment={equippedItems.armor_head}
                character={character}
                onUnequip={onUnequipItem}
              />
            </div>
            <div className="col-start-5">
              <EquipmentSlot
                slotName="weapon_off"
                equipment={equippedItems.weapon_off}
                character={character}
                onUnequip={onUnequipItem}
              />
            </div>

            {/* Row 3: Hands, Chest, Hands */}
            <div className="col-start-2">
              <EquipmentSlot
                slotName="armor_hands"
                equipment={equippedItems.armor_hands}
                character={character}
                onUnequip={onUnequipItem}
                size="sm"
              />
            </div>
            <div className="col-start-3">
              <EquipmentSlot
                slotName="armor_chest"
                equipment={equippedItems.armor_chest}
                character={character}
                onUnequip={onUnequipItem}
              />
            </div>

            {/* Row 4: Legs */}
            <div className="col-start-3">
              <EquipmentSlot
                slotName="armor_legs"
                equipment={equippedItems.armor_legs}
                character={character}
                onUnequip={onUnequipItem}
              />
            </div>

            {/* Row 5: Ring 1, Feet, Ring 2 */}
            <div className="col-start-1">
              <EquipmentSlot
                slotName="accessory_ring1"
                equipment={equippedItems.accessory_ring1}
                character={character}
                onUnequip={onUnequipItem}
                size="sm"
              />
            </div>
            <div className="col-start-3">
              <EquipmentSlot
                slotName="armor_feet"
                equipment={equippedItems.armor_feet}
                character={character}
                onUnequip={onUnequipItem}
              />
            </div>
            <div className="col-start-5">
              <EquipmentSlot
                slotName="accessory_ring2"
                equipment={equippedItems.accessory_ring2}
                character={character}
                onUnequip={onUnequipItem}
                size="sm"
              />
            </div>
          </div>
        </div>

        <Separator className="bg-gray-700" />

        {/* Character Stats */}
        <div>
          <h3 className="text-lg font-semibold text-white mb-3">Character Stats</h3>
          <div className="grid grid-cols-2 gap-4">
            {/* Primary Attributes */}
            <div>
              <h4 className="text-sm font-medium text-gray-400 mb-2">Attributes</h4>
              <div className="space-y-1 text-sm">
                <div className="flex justify-between">
                  <span className="text-gray-300">Might:</span>
                  <span className={getStatColor(character?.might || 0, totalStats.might)}>
                    {totalStats.might}{getStatBonus(character?.might || 0, totalStats.might)}
                  </span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-300">Intellect:</span>
                  <span className={getStatColor(character?.intellect || 0, totalStats.intellect)}>
                    {totalStats.intellect}{getStatBonus(character?.intellect || 0, totalStats.intellect)}
                  </span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-300">Will:</span>
                  <span className={getStatColor(character?.will || 0, totalStats.will)}>
                    {totalStats.will}{getStatBonus(character?.will || 0, totalStats.will)}
                  </span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-300">Shadow:</span>
                  <span className={getStatColor(character?.shadow || 0, totalStats.shadow)}>
                    {totalStats.shadow}{getStatBonus(character?.shadow || 0, totalStats.shadow)}
                  </span>
                </div>
              </div>
            </div>

            {/* Combat Stats */}
            <div>
              <h4 className="text-sm font-medium text-gray-400 mb-2">Combat</h4>
              <div className="space-y-1 text-sm">
                <div className="flex justify-between">
                  <span className="text-gray-300">Health:</span>
                  <span className={getStatColor(character?.health || 0, totalStats.health)}>
                    {totalStats.health}{getStatBonus(character?.health || 0, totalStats.health)}
                  </span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-300">Mana:</span>
                  <span className={getStatColor(character?.mana || 0, totalStats.mana)}>
                    {totalStats.mana}{getStatBonus(character?.mana || 0, totalStats.mana)}
                  </span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-300">Damage:</span>
                  <span className="text-green-400">
                    +{totalStats.damage}
                  </span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-300">Defense:</span>
                  <span className="text-blue-400">
                    +{totalStats.defense}
                  </span>
                </div>
              </div>
            </div>
          </div>

          {/* Corruption Stats */}
          <div className="mt-4">
            <h4 className="text-sm font-medium text-gray-400 mb-2">Corruption</h4>
            <div className="grid grid-cols-2 gap-4 text-sm">
              <div className="flex justify-between">
                <span className="text-gray-300">Current:</span>
                <span className="text-red-400">
                  {character?.corruption || 0}%
                </span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-300">Resistance:</span>
                <span className="text-blue-400">
                  +{totalStats.corruption_resistance}
                </span>
              </div>
            </div>
          </div>
        </div>

        <Separator className="bg-gray-700" />

        {/* Equipment Summary */}
        <div>
          <h3 className="text-lg font-semibold text-white mb-3">Equipment Summary</h3>
          <div className="grid grid-cols-1 gap-2 text-sm">
            {equipmentSlots.map(slot => {
              const item = equippedItems[slot.name];
              return (
                <div key={slot.name} className="flex justify-between items-center">
                  <span className="text-gray-400">{slot.label}:</span>
                  <span className={item ? 'text-white' : 'text-gray-600'}>
                    {item ? (
                      <span className="flex items-center gap-2">
                        {item.name}
                        <Badge 
                          className={`text-xs px-1 py-0 ${
                            item.rarity?.name === 'Common' ? 'bg-gray-500' :
                            item.rarity?.name === 'Uncommon' ? 'bg-green-500' :
                            item.rarity?.name === 'Rare' ? 'bg-blue-500' :
                            item.rarity?.name === 'Epic' ? 'bg-purple-500' :
                            item.rarity?.name === 'Legendary' ? 'bg-orange-500' :
                            'bg-gray-500'
                          } text-white`}
                        >
                          {item.rarity?.name?.charAt(0) || 'C'}
                        </Badge>
                      </span>
                    ) : (
                      'Empty'
                    )}
                  </span>
                </div>
              );
            })}
          </div>
        </div>
      </CardContent>
    </Card>
  );
};

export default CharacterEquipment;

