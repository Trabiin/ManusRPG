import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '../ui/card';
import { Button } from '../ui/button';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../ui/tabs';
import { Alert, AlertDescription } from '../ui/alert';
import { Badge } from '../ui/badge';
import CharacterEquipment from './CharacterEquipment';
import InventoryGrid from './InventoryGrid';

const EquipmentManager = ({ className = "" }) => {
  const [character, setCharacter] = useState(null);
  const [equippedItems, setEquippedItems] = useState({});
  const [availableItems, setAvailableItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [notification, setNotification] = useState(null);

  const API_BASE = 'http://localhost:5002/api';

  useEffect(() => {
    loadCharacterData();
    loadAvailableEquipment();
  }, []);

  const loadCharacterData = async () => {
    try {
      // For demo purposes, we'll create a mock character
      // In a real implementation, this would fetch from the API
      const mockCharacter = {
        id: 1,
        name: 'Test Drifter',
        level: 5,
        might: 12,
        intellect: 10,
        will: 14,
        shadow: 8,
        health: 120,
        mana: 80,
        corruption: 25
      };
      setCharacter(mockCharacter);

      // Load equipped items
      await loadEquippedItems();
    } catch (err) {
      setError('Failed to load character data');
      console.error('Character loading error:', err);
    }
  };

  const loadEquippedItems = async () => {
    try {
      const response = await fetch(`${API_BASE}/equipment/equipped`, {
        credentials: 'include'
      });
      
      if (response.ok) {
        const data = await response.json();
        setEquippedItems(data.equipped_items || {});
      } else {
        // If no session, start with empty equipment
        setEquippedItems({});
      }
    } catch (err) {
      console.error('Failed to load equipped items:', err);
      setEquippedItems({});
    }
  };

  const loadAvailableEquipment = async () => {
    try {
      setLoading(true);
      const response = await fetch(`${API_BASE}/equipment/available`);
      
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }
      
      const data = await response.json();
      
      // Add character eligibility check to each item
      const itemsWithEligibility = await Promise.all(
        data.items.map(async (item) => {
          try {
            const detailResponse = await fetch(`${API_BASE}/equipment/${item.item_id}`);
            if (detailResponse.ok) {
              const detailData = await detailResponse.json();
              return {
                ...item,
                ...detailData,
                can_equip: detailData.can_equip || false,
                equip_reason: detailData.equip_reason || ''
              };
            }
            return { ...item, can_equip: false, equip_reason: 'Unable to check requirements' };
          } catch (err) {
            return { ...item, can_equip: false, equip_reason: 'Error checking requirements' };
          }
        })
      );
      
      setAvailableItems(itemsWithEligibility);
    } catch (err) {
      setError(`Failed to load equipment: ${err.message}`);
      console.error('Equipment loading error:', err);
    } finally {
      setLoading(false);
    }
  };

  const equipItem = async (item) => {
    try {
      const response = await fetch(`${API_BASE}/equipment/equip`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        credentials: 'include',
        body: JSON.stringify({
          item_id: item.item_id
        })
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Failed to equip item');
      }

      const data = await response.json();
      
      // Update equipped items
      setEquippedItems(prev => ({
        ...prev,
        [item.slot]: item
      }));

      showNotification(`Equipped ${item.name}`, 'success');
      
      // Reload available items to update eligibility
      await loadAvailableEquipment();
      
    } catch (err) {
      showNotification(`Failed to equip ${item.name}: ${err.message}`, 'error');
      console.error('Equip error:', err);
    }
  };

  const unequipItem = async (slotName) => {
    try {
      const response = await fetch(`${API_BASE}/equipment/unequip`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        credentials: 'include',
        body: JSON.stringify({
          slot: slotName
        })
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Failed to unequip item');
      }

      const item = equippedItems[slotName];
      
      // Update equipped items
      setEquippedItems(prev => {
        const updated = { ...prev };
        delete updated[slotName];
        return updated;
      });

      showNotification(`Unequipped ${item?.name || 'item'}`, 'success');
      
      // Reload available items to update eligibility
      await loadAvailableEquipment();
      
    } catch (err) {
      showNotification(`Failed to unequip item: ${err.message}`, 'error');
      console.error('Unequip error:', err);
    }
  };

  const showNotification = (message, type = 'info') => {
    setNotification({ message, type });
    setTimeout(() => setNotification(null), 3000);
  };

  const getEquipmentStats = () => {
    const stats = {
      totalItems: Object.keys(equippedItems).length,
      totalSlots: 10,
      rarityBreakdown: {},
      corruptionItems: 0,
      totalBonuses: {
        might: 0,
        intellect: 0,
        will: 0,
        shadow: 0,
        damage: 0,
        defense: 0,
        health: 0,
        mana: 0
      }
    };

    Object.values(equippedItems).forEach(item => {
      if (item) {
        // Rarity breakdown
        const rarity = item.rarity?.name || 'Common';
        stats.rarityBreakdown[rarity] = (stats.rarityBreakdown[rarity] || 0) + 1;
        
        // Corruption items
        if (item.corruption_effect !== 0) {
          stats.corruptionItems++;
        }
        
        // Total bonuses
        if (item.stats) {
          Object.entries(item.stats).forEach(([stat, value]) => {
            if (stats.totalBonuses.hasOwnProperty(stat)) {
              stats.totalBonuses[stat] += value;
            }
          });
        }
      }
    });

    return stats;
  };

  if (loading) {
    return (
      <Card className={`bg-gray-900 border-gray-700 ${className}`}>
        <CardContent className="flex items-center justify-center h-64">
          <div className="text-white">Loading equipment...</div>
        </CardContent>
      </Card>
    );
  }

  if (error) {
    return (
      <Card className={`bg-gray-900 border-gray-700 ${className}`}>
        <CardContent className="p-6">
          <Alert className="border-red-500 bg-red-500/10">
            <AlertDescription className="text-red-400">
              {error}
            </AlertDescription>
          </Alert>
          <Button 
            onClick={() => {
              setError(null);
              loadCharacterData();
              loadAvailableEquipment();
            }}
            className="mt-4"
          >
            Retry
          </Button>
        </CardContent>
      </Card>
    );
  }

  const equipmentStats = getEquipmentStats();

  return (
    <div className={`space-y-4 ${className}`}>
      {/* Notification */}
      {notification && (
        <Alert className={`
          ${notification.type === 'success' ? 'border-green-500 bg-green-500/10' : 
            notification.type === 'error' ? 'border-red-500 bg-red-500/10' : 
            'border-blue-500 bg-blue-500/10'}
        `}>
          <AlertDescription className={`
            ${notification.type === 'success' ? 'text-green-400' : 
              notification.type === 'error' ? 'text-red-400' : 
              'text-blue-400'}
          `}>
            {notification.message}
          </AlertDescription>
        </Alert>
      )}

      {/* Equipment Stats Overview */}
      <Card className="bg-gray-900 border-gray-700">
        <CardHeader>
          <CardTitle className="text-white flex items-center justify-between">
            <span>Equipment Overview</span>
            <Badge variant="outline" className="text-gray-300">
              {equipmentStats.totalItems}/{equipmentStats.totalSlots} Equipped
            </Badge>
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
            <div className="text-center">
              <div className="text-2xl text-green-400 font-bold">
                +{equipmentStats.totalBonuses.damage}
              </div>
              <div className="text-gray-400">Total Damage</div>
            </div>
            <div className="text-center">
              <div className="text-2xl text-blue-400 font-bold">
                +{equipmentStats.totalBonuses.defense}
              </div>
              <div className="text-gray-400">Total Defense</div>
            </div>
            <div className="text-center">
              <div className="text-2xl text-purple-400 font-bold">
                +{equipmentStats.totalBonuses.might + equipmentStats.totalBonuses.intellect + 
                   equipmentStats.totalBonuses.will + equipmentStats.totalBonuses.shadow}
              </div>
              <div className="text-gray-400">Total Attributes</div>
            </div>
            <div className="text-center">
              <div className={`text-2xl font-bold ${equipmentStats.corruptionItems > 0 ? 'text-red-400' : 'text-gray-400'}`}>
                {equipmentStats.corruptionItems}
              </div>
              <div className="text-gray-400">Corrupted Items</div>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Main Equipment Interface */}
      <Tabs defaultValue="equipment" className="w-full">
        <TabsList className="grid w-full grid-cols-2 bg-gray-800">
          <TabsTrigger value="equipment" className="text-white data-[state=active]:bg-gray-700">
            Character Equipment
          </TabsTrigger>
          <TabsTrigger value="inventory" className="text-white data-[state=active]:bg-gray-700">
            Inventory ({availableItems.length})
          </TabsTrigger>
        </TabsList>

        <TabsContent value="equipment" className="mt-4">
          <CharacterEquipment
            character={character}
            equippedItems={equippedItems}
            onUnequipItem={unequipItem}
          />
        </TabsContent>

        <TabsContent value="inventory" className="mt-4">
          <InventoryGrid
            items={availableItems}
            character={character}
            onEquipItem={equipItem}
          />
        </TabsContent>
      </Tabs>
    </div>
  );
};

export default EquipmentManager;

