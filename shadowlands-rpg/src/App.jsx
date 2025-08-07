import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from './components/ui/card';
import { Button } from './components/ui/button';
import { Tabs, TabsContent, TabsList, TabsTrigger } from './components/ui/tabs';
import { Badge } from './components/ui/badge';
import EquipmentManager from './components/game/EquipmentManager';
import DialogueInterface from './components/game/DialogueInterface';

// Mobile Touch Interface Enhancement
// Ensure viewport meta tag is set in index.html:
// <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">

// Mobile Touch Interface Utilities
const handleTouchInteraction = (e, callback) => {
  if (e.type === 'touchend') {
    e.preventDefault();
    e.stopPropagation();
  }
  if (callback) callback(e);
};

const isTouchDevice = () => {
  return 'ontouchstart' in window || navigator.maxTouchPoints > 0;
};

function App() {
  const [activeTab, setActiveTab] = useState('character');
  const [dialogueOpen, setDialogueOpen] = useState(false);
  const [currentDialogue, setCurrentDialogue] = useState(null);

  // Handle dialogue interactions
  const handleOpenDialogue = (dialogueData) => {
    setCurrentDialogue(dialogueData);
    setDialogueOpen(true);
  };

  const handleCloseDialogue = () => {
    setDialogueOpen(false);
    setCurrentDialogue(null);
  };

  // Mobile-friendly touch handler
  const handleTabChange = (value) => {
    setActiveTab(value);
  };

  const handleDemoDialogue = (e) => {
    handleTouchInteraction(e, () => {
      handleOpenDialogue({
        name: 'Mysterious Stranger',
        portrait: '/api/placeholder/120/120',
        dialogue: 'The darkness is spreading. Will you join us, or stand against the coming tide?'
      });
    });
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-purple-900 to-gray-800 text-white relative overflow-hidden">
      {/* Background effects */}
      <div className="absolute inset-0 bg-black/20"></div>
      <div className="absolute top-0 left-0 w-full h-full bg-gradient-to-br from-purple-500/10 to-transparent"></div>
      
      {/* Main content */}
      <div className="relative z-10 container mx-auto px-4 py-6">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl md:text-6xl font-bold bg-gradient-to-r from-purple-400 to-pink-400 bg-clip-text text-transparent mb-2">
            Shadowlands
          </h1>
          <p className="text-lg md:text-xl text-gray-300">Dark Fantasy RPG</p>
          <Badge variant="outline" className="mt-2 border-purple-400 text-purple-300">
            Alpha Build
          </Badge>
        </div>

        {/* Main game interface */}
        <div className="max-w-6xl mx-auto">
          <Tabs value={activeTab} onValueChange={handleTabChange} className="w-full">
            <TabsList className="grid w-full grid-cols-4 mb-6 bg-gray-800/50 border border-gray-700">
              <TabsTrigger 
                value="character" 
                className="data-[state=active]:bg-purple-600 data-[state=active]:text-white touch-manipulation select-none min-h-[44px]"
                onTouchStart={(e) => e.preventDefault()}
              >
                Character
              </TabsTrigger>
              <TabsTrigger 
                value="equipment" 
                className="data-[state=active]:bg-purple-600 data-[state=active]:text-white touch-manipulation select-none min-h-[44px]"
                onTouchStart={(e) => e.preventDefault()}
              >
                Equipment
              </TabsTrigger>
              <TabsTrigger 
                value="quests" 
                className="data-[state=active]:bg-purple-600 data-[state=active]:text-white touch-manipulation select-none min-h-[44px]"
                onTouchStart={(e) => e.preventDefault()}
              >
                Quests
              </TabsTrigger>
              <TabsTrigger 
                value="world" 
                className="data-[state=active]:bg-purple-600 data-[state=active]:text-white touch-manipulation select-none min-h-[44px]"
                onTouchStart={(e) => e.preventDefault()}
              >
                World
              </TabsTrigger>
            </TabsList>

            <TabsContent value="character" className="space-y-6">
              <Card className="bg-gray-800/50 border-gray-700">
                <CardHeader>
                  <CardTitle className="text-purple-300">Character Overview</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div>
                      <h3 className="text-lg font-semibold mb-3 text-purple-200">Attributes</h3>
                      <div className="space-y-2">
                        <div className="flex justify-between">
                          <span>Might</span>
                          <span className="text-purple-300">12</span>
                        </div>
                        <div className="flex justify-between">
                          <span>Intellect</span>
                          <span className="text-purple-300">10</span>
                        </div>
                        <div className="flex justify-between">
                          <span>Will</span>
                          <span className="text-purple-300">8</span>
                        </div>
                        <div className="flex justify-between">
                          <span>Shadow</span>
                          <span className="text-purple-300">6</span>
                        </div>
                      </div>
                    </div>
                    <div>
                      <h3 className="text-lg font-semibold mb-3 text-purple-200">Status</h3>
                      <div className="space-y-2">
                        <div className="flex justify-between">
                          <span>Level</span>
                          <span className="text-green-400">3</span>
                        </div>
                        <div className="flex justify-between">
                          <span>Health</span>
                          <span className="text-red-400">185/185</span>
                        </div>
                        <div className="flex justify-between">
                          <span>Mana</span>
                          <span className="text-blue-400">85/85</span>
                        </div>
                        <div className="flex justify-between">
                          <span>Corruption</span>
                          <span className="text-purple-400">Pure</span>
                        </div>
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </TabsContent>

            <TabsContent value="equipment" className="space-y-6">
              <EquipmentManager />
            </TabsContent>

            <TabsContent value="quests" className="space-y-6">
              <Card className="bg-gray-800/50 border-gray-700">
                <CardHeader>
                  <CardTitle className="text-purple-300">Available Quests</CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-gray-400">Quest system coming soon...</p>
                </CardContent>
              </Card>
            </TabsContent>

            <TabsContent value="world" className="space-y-6">
              <Card className="bg-gray-800/50 border-gray-700">
                <CardHeader>
                  <CardTitle className="text-purple-300">World Exploration</CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-gray-400">World exploration coming soon...</p>
                </CardContent>
              </Card>
            </TabsContent>
          </Tabs>
        </div>
      </div>

      {/* Dialogue Interface */}
      {dialogueOpen && currentDialogue && (
        <DialogueInterface
          isOpen={dialogueOpen}
          onClose={handleCloseDialogue}
          character={currentDialogue}
          dialogue={currentDialogue.dialogue}
        />
      )}
      
      {/* Demo button to test dialogue - remove in production */}
      <Button
        onClick={handleDemoDialogue}
        onTouchEnd={handleDemoDialogue}
        className="fixed bottom-4 right-4 bg-yellow-600 hover:bg-yellow-700 focus:bg-yellow-700 active:bg-yellow-700 text-black px-4 py-2 rounded font-semibold z-40 min-h-[44px] min-w-[44px] touch-manipulation select-none"
        onTouchStart={(e) => e.preventDefault()}
      >
        Test Dialogue
      </Button>
    </div>
  );
}

export default App;

