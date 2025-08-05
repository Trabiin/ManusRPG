import React, { useState } from 'react';
import CharacterPortrait from './CharacterPortrait';
import ProgressBar from './ProgressBar';
import InventorySlot from './InventorySlot';
import GamePanel from './GamePanel';
import ActionButton from './ActionButton';
import { Sword, Shield, Zap, Eye, Map, Scroll, Settings, Menu, X } from 'lucide-react';

const MobileGameInterface = () => {
  const [character] = useState({
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

  const [showMenu, setShowMenu] = useState(false);
  const [activePanel, setActivePanel] = useState('game');

  const [inventory] = useState([
    { id: 1, name: 'Iron Sword', icon: '/api/placeholder/40/40', rarity: 'common', quantity: 1 },
    { id: 2, name: 'Corrupted Blade', icon: '/api/placeholder/40/40', rarity: 'rare', corruption: 5 },
    { id: 3, name: 'Health Potion', icon: '/api/placeholder/40/40', rarity: 'common', quantity: 3 },
    { id: 4, name: 'Shadow Crystal', icon: '/api/placeholder/40/40', rarity: 'epic', corruption: 10 }
  ]);

  const [quests] = useState([
    { id: 1, title: 'Into the Woods', description: 'Investigate the corrupted forest', progress: 2, maxProgress: 5 },
    { id: 2, title: 'Venter into Ioaes', description: 'Find the lost settlement', progress: 1, maxProgress: 3 }
  ]);

  const handleActionClick = (action) => {
    console.log('Action clicked:', action);
  };

  const renderCharacterPanel = () => (
    <GamePanel title="Character" corruption={character.corruption} className="h-full">
      <div className="space-y-4">
        <div className="flex items-center space-x-4">
          <CharacterPortrait 
            name={character.name}
            level={character.level}
            corruption={character.corruption}
            size="md"
          />
          <div className="flex-1 space-y-2">
            <ProgressBar 
              value={character.health}
              max={character.maxHealth}
              type="health"
              size="sm"
              corruption={character.corruption}
            />
            <ProgressBar 
              value={character.mana}
              max={character.maxMana}
              type="mana"
              size="sm"
              corruption={character.corruption}
            />
            <ProgressBar 
              value={character.corruption}
              max={100}
              type="corruption"
              size="sm"
              corruption={character.corruption}
            />
          </div>
        </div>

        <div className="grid grid-cols-2 gap-2 text-sm">
          <div className="bg-gray-800/50 p-2 rounded text-center">
            <div className="text-gray-400">Might</div>
            <div className="text-yellow-400 font-bold">{character.attributes.might}</div>
          </div>
          <div className="bg-gray-800/50 p-2 rounded text-center">
            <div className="text-gray-400">Intellect</div>
            <div className="text-blue-400 font-bold">{character.attributes.intellect}</div>
          </div>
          <div className="bg-gray-800/50 p-2 rounded text-center">
            <div className="text-gray-400">Will</div>
            <div className="text-green-400 font-bold">{character.attributes.will}</div>
          </div>
          <div className="bg-gray-800/50 p-2 rounded text-center">
            <div className="text-gray-400">Shadow</div>
            <div className="text-red-400 font-bold">{character.attributes.shadow}</div>
          </div>
        </div>
      </div>
    </GamePanel>
  );

  const renderInventoryPanel = () => (
    <GamePanel title="Inventory" corruption={character.corruption} className="h-full">
      <div className="grid grid-cols-4 gap-2">
        {Array.from({ length: 12 }, (_, i) => (
          <InventorySlot 
            key={i}
            item={inventory[i]}
            size="md"
          />
        ))}
      </div>
    </GamePanel>
  );

  const renderQuestsPanel = () => (
    <GamePanel title="Quests" corruption={character.corruption} className="h-full">
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
  );

  const renderGameArea = () => (
    <div className="relative h-full bg-gradient-to-b from-gray-900/50 to-gray-800/50 rounded-lg flex items-center justify-center">
      <div className="text-center text-gray-300 p-4">
        <h2 className="text-xl font-bold font-primary mb-4">The Corrupted Forest</h2>
        <p className="text-base mb-6">Dark mists swirl between twisted trees...</p>
        <div className="space-y-3">
          <ActionButton 
            variant="primary" 
            onClick={() => handleActionClick('explore')}
            icon={<Eye size={18} />}
            className="w-full"
          >
            Explore Deeper
          </ActionButton>
          <ActionButton 
            variant="corrupted" 
            onClick={() => handleActionClick('shadow')}
            icon={<Zap size={18} />}
            corruption={character.corruption}
            className="w-full"
          >
            Use Shadow Magic
          </ActionButton>
        </div>
      </div>
    </div>
  );

  return (
    <div className="min-h-screen flex flex-col">
      {/* Mobile Header */}
      <div className="flex items-center justify-between p-4 bg-gray-800/90 backdrop-blur-sm">
        <button
          onClick={() => setShowMenu(!showMenu)}
          className="p-2 text-gray-300 hover:text-white"
        >
          {showMenu ? <X size={24} /> : <Menu size={24} />}
        </button>
        <h1 className="text-lg font-bold font-primary text-gray-200">Shadowlands</h1>
        <div className="w-10" /> {/* Spacer */}
      </div>

      {/* Mobile Menu Overlay */}
      {showMenu && (
        <div className="fixed inset-0 bg-black/50 z-50 flex">
          <div className="w-80 bg-gray-800 p-4 space-y-4">
            <button
              onClick={() => {
                setActivePanel('character');
                setShowMenu(false);
              }}
              className="w-full text-left p-3 bg-gray-700 rounded text-gray-200 hover:bg-gray-600"
            >
              Character
            </button>
            <button
              onClick={() => {
                setActivePanel('inventory');
                setShowMenu(false);
              }}
              className="w-full text-left p-3 bg-gray-700 rounded text-gray-200 hover:bg-gray-600"
            >
              Inventory
            </button>
            <button
              onClick={() => {
                setActivePanel('quests');
                setShowMenu(false);
              }}
              className="w-full text-left p-3 bg-gray-700 rounded text-gray-200 hover:bg-gray-600"
            >
              Quests
            </button>
            <button
              onClick={() => {
                setActivePanel('game');
                setShowMenu(false);
              }}
              className="w-full text-left p-3 bg-gray-700 rounded text-gray-200 hover:bg-gray-600"
            >
              Game
            </button>
          </div>
          <div 
            className="flex-1"
            onClick={() => setShowMenu(false)}
          />
        </div>
      )}

      {/* Main Content Area */}
      <div className="flex-1 p-4">
        {activePanel === 'character' && renderCharacterPanel()}
        {activePanel === 'inventory' && renderInventoryPanel()}
        {activePanel === 'quests' && renderQuestsPanel()}
        {activePanel === 'game' && renderGameArea()}
      </div>

      {/* Mobile Action Bar */}
      <div className="p-4 bg-gray-800/90 backdrop-blur-sm">
        <GamePanel corruption={character.corruption} padding="sm">
          <div className="flex items-center justify-between">
            <div className="flex space-x-2">
              <ActionButton 
                variant="primary"
                size="sm"
                onClick={() => handleActionClick('attack')}
                icon={<Sword size={16} />}
              >
                Attack
              </ActionButton>
              <ActionButton 
                variant="primary"
                size="sm"
                onClick={() => handleActionClick('defend')}
                icon={<Shield size={16} />}
              >
                Defend
              </ActionButton>
              <ActionButton 
                variant="corrupted"
                size="sm"
                onClick={() => handleActionClick('shadow_strike')}
                icon={<Zap size={16} />}
                corruption={character.corruption}
              >
                Shadow
              </ActionButton>
            </div>

            <div className="flex space-x-1">
              <ActionButton 
                variant="primary"
                size="sm"
                onClick={() => handleActionClick('map')}
                icon={<Map size={16} />}
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

export default MobileGameInterface;

