import React, { useState } from 'react';
import GamePanel from './GamePanel';
import ActionButton from './ActionButton';
import { Skull, Sun, Sword, Book, Eye, Shield } from 'lucide-react';

const DialogueInterface = ({ 
  npc = {
    name: 'Mysterious Stranger',
    portrait: '/api/placeholder/120/120',
    dialogue: 'The darkness is spreading. Will you join us, or stand against the coming tide?'
  },
  choices = [],
  onChoiceSelect = () => {},
  onClose = () => {},
  corruption = 0
}) => {
  const [selectedChoice, setSelectedChoice] = useState(null);

  const defaultChoices = [
    {
      id: 1,
      text: 'I will embrace the darkness.',
      type: 'corruption',
      icon: <Skull size={16} />,
      corruptionChange: +5,
      requirements: null
    },
    {
      id: 2,
      text: 'I will resist the darkness.',
      type: 'pure',
      icon: <Sun size={16} />,
      corruptionChange: -2,
      requirements: null
    },
    {
      id: 3,
      text: 'How can I help you?',
      type: 'neutral',
      icon: <Eye size={16} />,
      corruptionChange: 0,
      requirements: null
    },
    {
      id: 4,
      text: 'I will gqrophe',
      type: 'corruption',
      icon: <Skull size={16} />,
      corruptionChange: +10,
      requirements: { corruption: 25 }
    },
    {
      id: 5,
      text: 'Leave me be.',
      type: 'neutral',
      icon: <Shield size={16} />,
      corruptionChange: 0,
      requirements: null
    }
  ];

  const activeChoices = choices.length > 0 ? choices : defaultChoices;

  const getChoiceVariant = (choice) => {
    switch (choice.type) {
      case 'corruption':
        return 'corrupted';
      case 'pure':
        return 'pure';
      case 'combat':
        return 'danger';
      default:
        return 'primary';
    }
  };

  const isChoiceAvailable = (choice) => {
    if (!choice.requirements) return true;
    
    if (choice.requirements.corruption && corruption < choice.requirements.corruption) {
      return false;
    }
    
    return true;
  };

  const handleChoiceClick = (choice) => {
    if (!isChoiceAvailable(choice)) return;
    
    setSelectedChoice(choice.id);
    setTimeout(() => {
      onChoiceSelect(choice);
    }, 200);
  };

  return (
    <div className="fixed inset-0 bg-black/80 flex items-center justify-center z-50 p-4">
      <div className="w-full max-w-4xl max-h-[90vh] overflow-hidden">
        <GamePanel corruption={corruption} className="h-full">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 h-full">
            {/* NPC Portrait */}
            <div className="flex flex-col items-center space-y-4">
              <div className="w-32 h-32 rounded-lg overflow-hidden border-2 border-gray-600">
                <img 
                  src={npc.portrait}
                  alt={npc.name}
                  className="w-full h-full object-cover"
                  onError={(e) => {
                    e.target.src = 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTIwIiBoZWlnaHQ9IjEyMCIgdmlld0JveD0iMCAwIDEyMCAxMjAiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxyZWN0IHdpZHRoPSIxMjAiIGhlaWdodD0iMTIwIiBmaWxsPSIjMkMyQzJDIi8+CjxjaXJjbGUgY3g9IjYwIiBjeT0iNDUiIHI9IjE1IiBmaWxsPSIjNEE0QTRBIi8+CjxwYXRoIGQ9Ik0zMCA5MEM0MCA4MCA4MCA4MCA5MCA5MEw5MCA5MEgzMFoiIGZpbGw9IiM0QTRBNEEiLz4KPC9zdmc+';
                  }}
                />
              </div>
              <h3 className="text-lg font-semibold text-gray-200 font-primary text-center">
                {npc.name}
              </h3>
            </div>

            {/* Dialogue Text */}
            <div className="md:col-span-2 flex flex-col justify-between">
              <div className="bg-gray-800/50 p-6 rounded-lg mb-6">
                <p className="text-gray-200 text-lg leading-relaxed font-secondary">
                  {npc.dialogue}
                </p>
              </div>

              {/* Choice Buttons */}
              <div className="space-y-3">
                {activeChoices.map((choice) => {
                  const isAvailable = isChoiceAvailable(choice);
                  const isSelected = selectedChoice === choice.id;
                  
                  return (
                    <div key={choice.id} className="relative">
                      <ActionButton
                        variant={getChoiceVariant(choice)}
                        onClick={() => handleChoiceClick(choice)}
                        disabled={!isAvailable}
                        icon={choice.icon}
                        corruption={corruption}
                        className={`
                          w-full text-left justify-start
                          ${isSelected ? 'ring-2 ring-yellow-500' : ''}
                          ${!isAvailable ? 'opacity-50 cursor-not-allowed' : ''}
                        `}
                      >
                        <span className="flex-1">{choice.text}</span>
                        {choice.corruptionChange !== 0 && (
                          <span className={`
                            text-xs px-2 py-1 rounded
                            ${choice.corruptionChange > 0 
                              ? 'bg-red-900/50 text-red-300' 
                              : 'bg-green-900/50 text-green-300'
                            }
                          `}>
                            {choice.corruptionChange > 0 ? '+' : ''}{choice.corruptionChange}
                          </span>
                        )}
                      </ActionButton>
                      
                      {!isAvailable && choice.requirements && (
                        <div className="absolute right-2 top-1/2 transform -translate-y-1/2">
                          <span className="text-xs text-red-400">
                            Requires {choice.requirements.corruption}+ Corruption
                          </span>
                        </div>
                      )}
                    </div>
                  );
                })}
              </div>

              {/* Close Button */}
              <div className="mt-6 flex justify-end">
                <ActionButton
                  variant="primary"
                  onClick={onClose}
                  size="sm"
                >
                  Close
                </ActionButton>
              </div>
            </div>
          </div>
        </GamePanel>
      </div>
    </div>
  );
};

export default DialogueInterface;

