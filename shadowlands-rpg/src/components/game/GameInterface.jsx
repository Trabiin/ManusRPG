import React, { useState } from 'react';
import CharacterPortrait from './CharacterPortrait';
import ProgressBar from './ProgressBar';
import InventorySlot from './InventorySlot';
import GamePanel from './GamePanel';
import ActionButton from './ActionButton';
import { Sword, Shield, Zap, Eye, Map, Scroll, Settings } from 'lucide-react';

const GameInterface = () => {
  const [character, setCharacter] = useState({
    name: 'Kael Shadowbane',
    level: 15,
    corruption: 42,
    health: 142,
    maxHealth: 200,
    mana: 55,
    maxMana: 85,
    attributes: {
      might: 15,
      intellect: 9,
      will: 12,
      shadow: 18
    }
  });

  const [inventory] = useState([
    { id: 1, name: 'Iron Sword', icon: '/api/placeholder/40/40', rarity: 'common', quantity: 1 },
    { id: 2, name: 'Corrupted Blade', icon: '/api/placeholder/40/40', rarity: 'rare', corruption: 5 },
    { id: 3, name: 'Health Potion', icon: '/api/placeholder/40/40', rarity: 'common', quantity: 3 },
    { id: 4, name: 'Shadow Crystal', icon: '/api/placeholder/40/40', rarity: 'epic', corruption: 10 },
    { id: 5, name: 'Ancient Tome', icon: '/api/placeholder/40/40', rarity: 'legendary' }
  ]);

  const [quests] = useState([
    { id: 1, title: 'Into the Woods', description: 'Investigate the corrupted forest', progress: 2, maxProgress: 5 },
    { id: 2, title: 'Venter into Ioaes', description: 'Find the lost settlement', progress: 1, maxProgress: 3 }
  ]);

  const handleItemClick = (item) => {
    console.log('Item clicked:', item);
  };

  const handleActionClick = (action) => {
    console.log('Action clicked:', action);
  };

  return (
    <div className="game-layout min-h-screen">
      {/* Left Sidebar - Character Info */}
      <div className="game-sidebar">
        <GamePanel title="Character" corruption={character.corruption}>
          <div className="space-y-4">
            <CharacterPortrait 
              name={character.name}
              level={character.level}
              corruption={character.corruption}
              size="lg"
            />
            
            <div className="space-y-3">
              <ProgressBar 
                value={character.health}
                max={character.maxHealth}
                type="health"
                label="Health"
                corruption={character.corruption}
              />
              
              <ProgressBar 
                value={character.mana}
                max={character.maxMana}
                type="mana"
                label="Mana"
                corruption={character.corruption}
              />
              
              <ProgressBar 
                value={character.corruption}
                max={100}
                type="corruption"
                label="Corruption"
                corruption={character.corruption}
              />
            </div>

            <div className="grid grid-cols-2 gap-2 text-sm">
              <div className="bg-gray-800/50 p-2 rounded">
                <div className="text-gray-400">Might</div>
                <div className="text-yellow-400 font-bold">{character.attributes.might}</div>
              </div>
              <div className="bg-gray-800/50 p-2 rounded">
                <div className="text-gray-400">Intellect</div>
                <div className="text-blue-400 font-bold">{character.attributes.intellect}</div>
              </div>
              <div className="bg-gray-800/50 p-2 rounded">
                <div className="text-gray-400">Will</div>
                <div className="text-green-400 font-bold">{character.attributes.will}</div>
              </div>
              <div className="bg-gray-800/50 p-2 rounded">
                <div className="text-gray-400">Shadow</div>
                <div className="text-red-400 font-bold">{character.attributes.shadow}</div>
              </div>
            </div>
          </div>
        </GamePanel>
      </div>

      {/* Main Game Area */}
      <div className="game-main relative">
        <div className="absolute inset-0 bg-gradient-to-b from-gray-900/50 to-gray-800/50 flex items-center justify-center">
          <div className="text-center text-gray-300">
            <h2 className="text-2xl font-bold font-primary mb-4">The Corrupted Forest</h2>
            <p className="text-lg mb-6">Dark mists swirl between twisted trees...</p>
            <div className="space-y-2">
              <ActionButton 
                variant="primary" 
                onClick={() => handleActionClick('explore')}
                icon={<Eye size={20} />}
              >
                Explore Deeper
              </ActionButton>
              <ActionButton 
                variant="corrupted" 
                onClick={() => handleActionClick('shadow')}
                icon={<Zap size={20} />}
                corruption={character.corruption}
              >
                Use Shadow Magic
              </ActionButton>
            </div>
          </div>
        </div>
      </div>

      {/* Right Sidebar - Quests and Map */}
      <div className="game-questpanel space-y-4">
        <GamePanel title="Quests" corruption={character.corruption}>
          <div className="space-y-3">
            {quests.map(quest => (
              <div key={quest.id} className="bg-gray-800/50 p-3 rounded">
                <h4 className="font-semibold text-gray-200 font-primary">{quest.title}</h4>
                <p className="text-sm text-gray-400 mb-2">{quest.description}</p>
                <ProgressBar 
                  value={quest.progress}
                  max={quest.maxProgress}
                  type="experience"
                  size="sm"
                  showText={false}
                />
                <div className="text-xs text-gray-500 mt-1">
                  {quest.progress}/{quest.maxProgress}
                </div>
              </div>
            ))}
          </div>
        </GamePanel>

        <GamePanel title="Inventory" corruption={character.corruption}>
          <div className="grid grid-cols-4 gap-2">
            {Array.from({ length: 16 }, (_, i) => (
              <InventorySlot 
                key={i}
                item={inventory[i]}
                onClick={handleItemClick}
                size="md"
              />
            ))}
          </div>
        </GamePanel>
      </div>

      {/* Bottom Action Bar */}
      <div className="game-actionbar">
        <GamePanel className="h-full" corruption={character.corruption}>
          <div className="flex items-center justify-between h-full">
            <div className="flex items-center space-x-4">
              <ActionButton 
                variant="primary"
                onClick={() => handleActionClick('attack')}
                icon={<Sword size={20} />}
              >
                Attack
              </ActionButton>
              <ActionButton 
                variant="primary"
                onClick={() => handleActionClick('defend')}
                icon={<Shield size={20} />}
              >
                Defend
              </ActionButton>
              <ActionButton 
                variant="corrupted"
                onClick={() => handleActionClick('shadow_strike')}
                icon={<Zap size={20} />}
                corruption={character.corruption}
              >
                Shadow Strike
              </ActionButton>
            </div>

            <div className="flex items-center space-x-2">
              <ActionButton 
                variant="primary"
                size="sm"
                onClick={() => handleActionClick('map')}
                icon={<Map size={16} />}
              />
              <ActionButton 
                variant="primary"
                size="sm"
                onClick={() => handleActionClick('journal')}
                icon={<Scroll size={16} />}
              />
              <ActionButton 
                variant="primary"
                size="sm"
                onClick={() => handleActionClick('settings')}
                icon={<Settings size={16} />}
              />
            </div>
          </div>
        </GamePanel>
      </div>
    </div>
  );
};

export default GameInterface;

