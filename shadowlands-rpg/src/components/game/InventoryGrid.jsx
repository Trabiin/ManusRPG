import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '../ui/card';
import { Button } from '../ui/button';
import { Badge } from '../ui/badge';
import { Input } from '../ui/input';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../ui/select';
import EquipmentTooltip from './EquipmentTooltip';

const InventoryGrid = ({ 
  items = [], 
  character, 
  onEquipItem, 
  onItemAction,
  className = "" 
}) => {
  const [filteredItems, setFilteredItems] = useState(items);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterType, setFilterType] = useState('all');
  const [filterRarity, setFilterRarity] = useState('all');
  const [sortBy, setSortBy] = useState('name');
  const [showTooltip, setShowTooltip] = useState(false);
  const [tooltipPosition, setTooltipPosition] = useState({ x: 0, y: 0 });
  const [hoveredItem, setHoveredItem] = useState(null);

  useEffect(() => {
    let filtered = [...items];

    // Search filter
    if (searchTerm) {
      filtered = filtered.filter(item => 
        item.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        item.type.toLowerCase().includes(searchTerm.toLowerCase())
      );
    }

    // Type filter
    if (filterType !== 'all') {
      filtered = filtered.filter(item => item.type === filterType);
    }

    // Rarity filter
    if (filterRarity !== 'all') {
      filtered = filtered.filter(item => item.rarity?.name === filterRarity);
    }

    // Sort
    filtered.sort((a, b) => {
      switch (sortBy) {
        case 'name':
          return a.name.localeCompare(b.name);
        case 'level':
          return b.level - a.level;
        case 'rarity':
          const rarityOrder = { 'Common': 1, 'Uncommon': 2, 'Rare': 3, 'Epic': 4, 'Legendary': 5 };
          return (rarityOrder[b.rarity?.name] || 0) - (rarityOrder[a.rarity?.name] || 0);
        case 'type':
          return a.type.localeCompare(b.type);
        default:
          return 0;
      }
    });

    setFilteredItems(filtered);
  }, [items, searchTerm, filterType, filterRarity, sortBy]);

  const getRarityColor = (rarity) => {
    const colors = {
      'Common': 'border-gray-500 bg-gray-500/10',
      'Uncommon': 'border-green-500 bg-green-500/10',
      'Rare': 'border-blue-500 bg-blue-500/10',
      'Epic': 'border-purple-500 bg-purple-500/10',
      'Legendary': 'border-orange-500 bg-orange-500/10'
    };
    return colors[rarity] || 'border-gray-500 bg-gray-500/10';
  };

  const getTypeIcon = (type) => {
    const icons = {
      'weapon': '⚔️',
      'armor': '🛡️',
      'accessory': '💍',
      'consumable': '🧪',
      'material': '🔧'
    };
    return icons[type] || '📦';
  };

  const handleItemMouseEnter = (item, e) => {
    setHoveredItem(item);
    setTooltipPosition({ x: e.clientX, y: e.clientY });
    setShowTooltip(true);
  };

  const handleItemMouseLeave = () => {
    setShowTooltip(false);
    setHoveredItem(null);
  };

  const handleItemMouseMove = (e) => {
    if (showTooltip) {
      setTooltipPosition({ x: e.clientX, y: e.clientY });
    }
  };

  const handleEquipItem = (item) => {
    if (item.can_equip && onEquipItem) {
      onEquipItem(item);
    }
  };

  const uniqueTypes = [...new Set(items.map(item => item.type))];
  const uniqueRarities = [...new Set(items.map(item => item.rarity?.name).filter(Boolean))];

  return (
    <>
      <Card className={`bg-gray-900 border-gray-700 ${className}`}>
        <CardHeader>
          <CardTitle className="text-white flex items-center justify-between">
            <span>Inventory ({filteredItems.length}/{items.length})</span>
            <Badge variant="outline" className="text-gray-300">
              {character?.name || 'Character'}
            </Badge>
          </CardTitle>
          
          {/* Filters and Search */}
          <div className="grid grid-cols-1 md:grid-cols-4 gap-2 mt-4">
            <Input
              placeholder="Search items..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="bg-gray-800 border-gray-600 text-white"
            />
            
            <Select value={filterType} onValueChange={setFilterType}>
              <SelectTrigger className="bg-gray-800 border-gray-600 text-white">
                <SelectValue placeholder="Filter by type" />
              </SelectTrigger>
              <SelectContent className="bg-gray-800 border-gray-600">
                <SelectItem value="all">All Types</SelectItem>
                {uniqueTypes.map(type => (
                  <SelectItem key={type} value={type} className="text-white">
                    {getTypeIcon(type)} {type.charAt(0).toUpperCase() + type.slice(1)}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>

            <Select value={filterRarity} onValueChange={setFilterRarity}>
              <SelectTrigger className="bg-gray-800 border-gray-600 text-white">
                <SelectValue placeholder="Filter by rarity" />
              </SelectTrigger>
              <SelectContent className="bg-gray-800 border-gray-600">
                <SelectItem value="all">All Rarities</SelectItem>
                {uniqueRarities.map(rarity => (
                  <SelectItem key={rarity} value={rarity} className="text-white">
                    {rarity}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>

            <Select value={sortBy} onValueChange={setSortBy}>
              <SelectTrigger className="bg-gray-800 border-gray-600 text-white">
                <SelectValue placeholder="Sort by" />
              </SelectTrigger>
              <SelectContent className="bg-gray-800 border-gray-600">
                <SelectItem value="name" className="text-white">Name</SelectItem>
                <SelectItem value="level" className="text-white">Level</SelectItem>
                <SelectItem value="rarity" className="text-white">Rarity</SelectItem>
                <SelectItem value="type" className="text-white">Type</SelectItem>
              </SelectContent>
            </Select>
          </div>
        </CardHeader>

        <CardContent>
          {filteredItems.length === 0 ? (
            <div className="text-center text-gray-400 py-8">
              <div className="text-4xl mb-2">📦</div>
              <p>No items found</p>
              {searchTerm && (
                <p className="text-sm mt-1">Try adjusting your search or filters</p>
              )}
            </div>
          ) : (
            <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-3">
              {filteredItems.map((item, index) => (
                <Card
                  key={`${item.item_id}-${index}`}
                  className={`
                    relative cursor-pointer transition-all duration-200 
                    hover:scale-105 hover:shadow-lg
                    ${getRarityColor(item.rarity?.name)}
                    ${item.can_equip ? 'hover:border-green-400' : 'hover:border-red-400'}
                  `}
                  onMouseEnter={(e) => handleItemMouseEnter(item, e)}
                  onMouseLeave={handleItemMouseLeave}
                  onMouseMove={handleItemMouseMove}
                  onClick={() => handleEquipItem(item)}
                >
                  <CardContent className="p-3 flex flex-col items-center text-center">
                    {/* Item Icon */}
                    <div className="text-2xl mb-2">
                      {getTypeIcon(item.type)}
                    </div>

                    {/* Item Name */}
                    <div className="text-sm font-medium text-white mb-1 leading-tight">
                      {item.name.length > 14 
                        ? item.name.substring(0, 12) + '...' 
                        : item.name
                      }
                    </div>

                    {/* Level and Rarity */}
                    <div className="flex items-center justify-between w-full mb-2">
                      <Badge variant="outline" className="text-xs px-1 py-0">
                        Lv.{item.level}
                      </Badge>
                      <Badge 
                        className={`
                          text-xs px-1 py-0 
                          ${getRarityColor(item.rarity?.name).replace('border-', 'bg-').replace('/10', '/80')} 
                          text-white
                        `}
                      >
                        {item.rarity?.name?.charAt(0) || 'C'}
                      </Badge>
                    </div>

                    {/* Primary Stat */}
                    {item.stats && (
                      <div className="text-xs text-gray-300">
                        {Object.entries(item.stats).find(([_, value]) => value > 0) && (
                          <div>
                            {(() => {
                              const [stat, value] = Object.entries(item.stats).find(([_, v]) => v > 0) || ['', 0];
                              return `+${value} ${stat.replace('_', ' ')}`;
                            })()}
                          </div>
                        )}
                      </div>
                    )}

                    {/* Equip Status Indicator */}
                    <div className={`
                      absolute top-1 right-1 w-2 h-2 rounded-full
                      ${item.can_equip ? 'bg-green-500' : 'bg-red-500'}
                    `} />

                    {/* Corruption Indicator */}
                    {item.corruption_effect !== 0 && (
                      <div className={`
                        absolute top-1 left-1 w-2 h-2 rounded-full
                        ${item.corruption_effect > 0 ? 'bg-red-500' : 'bg-blue-500'}
                      `} />
                    )}

                    {/* Durability Bar */}
                    {item.durability < item.max_durability && (
                      <div className="absolute bottom-1 left-1 right-1 h-1 bg-gray-700 rounded-full overflow-hidden">
                        <div 
                          className={`h-full transition-all duration-300 ${
                            item.durability / item.max_durability > 0.5 
                              ? 'bg-green-500' 
                              : item.durability / item.max_durability > 0.25 
                                ? 'bg-yellow-500' 
                                : 'bg-red-500'
                          }`}
                          style={{ 
                            width: `${(item.durability / item.max_durability) * 100}%` 
                          }}
                        />
                      </div>
                    )}
                  </CardContent>
                </Card>
              ))}
            </div>
          )}
        </CardContent>
      </Card>

      <EquipmentTooltip
        equipment={hoveredItem}
        character={character}
        position={tooltipPosition}
        visible={showTooltip}
      />
    </>
  );
};

export default InventoryGrid;

